from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from trips.models import Trip
from seats.models import Seat
from .models import Reservation
from .serializers import ReservationSerializer, CreateReservationSerializer
from .pagination import StandardPagination


def error_response(code: str, message: str, details=None, http_status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {"error": {"code": code, "message": message, "details": details or {}}},
        status=http_status,
    )


class ReservationsRootView(APIView):
    """
    POST /api/reservations  -> create reservation (atomic)
    GET  /api/reservations  -> list my reservations (history)
    """

    def post(self, request):
        ser = CreateReservationSerializer(data=request.data)
        if not ser.is_valid():
            return error_response(
                code="VALIDATION_ERROR",
                message="Invalid input.",
                details=ser.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        trip_id = ser.validated_data["trip_id"]
        seat_ids = ser.validated_data["seat_ids"]

        # 1) Trip existence
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return error_response(
                code="NOT_FOUND",
                message="Trip not found.",
                details={"trip_id": trip_id},
                http_status=status.HTTP_404_NOT_FOUND,
            )

        if trip.status == "cancelled":
            return error_response(
                code="TRIP_CANCELLED",
                message="Trip is cancelled.",
                details={"trip_id": trip_id},
                http_status=status.HTTP_409_CONFLICT,
            )

        # 2) Atomic transaction + row locking
        with transaction.atomic():
            # Lock all requested seats
            seats_qs = Seat.objects.select_for_update().filter(id__in=seat_ids)

            found_ids = set(seats_qs.values_list("id", flat=True))
            missing = [sid for sid in seat_ids if sid not in found_ids]
            if missing:
                return error_response(
                    code="NOT_FOUND",
                    message="One or more seats not found.",
                    details={"seat_ids": missing},
                    http_status=status.HTTP_404_NOT_FOUND,
                )

            wrong_trip = list(seats_qs.exclude(trip_id=trip_id).values_list("id", flat=True))
            if wrong_trip:
                return error_response(
                    code="CONFLICT",
                    message="One or more seats do not belong to this trip.",
                    details={"seat_ids": wrong_trip, "trip_id": trip_id},
                    http_status=status.HTTP_409_CONFLICT,
                )

            conflicted = list(seats_qs.exclude(status="available").values_list("id", flat=True))
            if conflicted:
                return error_response(
                    code="SEAT_CONFLICT",
                    message="One or more seats are already reserved.",
                    details={"seat_ids": conflicted},
                    http_status=status.HTTP_409_CONFLICT,
                )

            # Optional: if booking after departure should be blocked
            if timezone.now() >= trip.departure_time:
                return error_response(
                    code="TRIP_DEPARTED",
                    message="Trip already departed.",
                    details={"trip_id": trip_id},
                    http_status=status.HTTP_409_CONFLICT,
                )

            # 3) Create reservation
            reservation = Reservation.objects.create(
                user=request.user,
                trip=trip,
                status="active",
            )
            reservation.seats.add(*list(seats_qs))

            # 4) Mark seats reserved
            seats_qs.update(status="reserved")

        return Response(
            {"reservation": ReservationSerializer(reservation).data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        status_param = request.query_params.get("status")
        qs = Reservation.objects.filter(user=request.user).order_by("-created_at")

        if status_param:
            qs = qs.filter(status=status_param)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = ReservationSerializer(page, many=True).data

        # API_SPEC history response: meta + items
        return Response(
            {
                "meta": {
                    "page": paginator.page.number,
                    "page_size": paginator.get_page_size(request),
                    "total": paginator.page.paginator.count,
                },
                "items": [
                    {
                        "reservation_id": item["reservation_id"],
                        "trip_id": item["trip_id"],
                        "status": item["status"],
                        "seat_ids": item["seat_ids"],
                        "created_at": item["created_at"],
                    }
                    for item in data
                ],
            },
            status=200,
        )


class ReservationItemView(APIView):
    """
    GET    /api/reservations/{reservationId} -> details (owner only)
    DELETE /api/reservations/{reservationId} -> cancel (owner only, if active & before departure)
    """

    def get(self, request, reservation_id: int):
        try:
            r = Reservation.objects.prefetch_related("seats").select_related("trip").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return error_response(
                code="NOT_FOUND",
                message="Reservation not found.",
                details={"reservation_id": reservation_id},
                http_status=status.HTTP_404_NOT_FOUND,
            )

        if r.user_id != request.user.id:
            return error_response(
                code="FORBIDDEN",
                message="You do not have access to this reservation.",
                details={},
                http_status=status.HTTP_403_FORBIDDEN,
            )

        return Response({"reservation": ReservationSerializer(r).data}, status=200)

    def delete(self, request, reservation_id: int):
        try:
            r = Reservation.objects.select_related("trip").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return error_response(
                code="NOT_FOUND",
                message="Reservation not found.",
                details={"reservation_id": reservation_id},
                http_status=status.HTTP_404_NOT_FOUND,
            )

        if r.user_id != request.user.id:
            return error_response(
                code="FORBIDDEN",
                message="You do not have access to this reservation.",
                details={},
                http_status=status.HTTP_403_FORBIDDEN,
            )

        if r.status != "active":
            return error_response(
                code="RESERVATION_NOT_CANCELLABLE",
                message="Reservation cannot be cancelled at this time.",
                details={"reason": "NOT_ACTIVE"},
                http_status=status.HTTP_409_CONFLICT,
            )

        now = timezone.now()
        if now >= r.trip.departure_time:
            return error_response(
                code="RESERVATION_NOT_CANCELLABLE",
                message="Reservation cannot be cancelled at this time.",
                details={"reason": "AFTER_DEPARTURE"},
                http_status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():
            # Lock seats and release them
            seats_qs = Seat.objects.select_for_update().filter(reservations=r)

            r.status = "cancelled"
            r.cancelled_at = timezone.now()
            r.save(update_fields=["status", "cancelled_at"])

            seats_qs.update(status="available")

        return Response(
            {"reservation": {"reservation_id": r.id, "status": r.status, "cancelled_at": r.cancelled_at}},
            status=200,
        )
