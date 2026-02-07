from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from trips.models import Trip
from .models import Seat
from .serializers import SeatSerializer


def error_response(code: str, message: str, details=None, http_status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {"error": {"code": code, "message": message, "details": details or {}}},
        status=http_status,
    )


class TripSeatMapView(APIView):
    def get(self, request, trip_id: int):
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return error_response(
                code="NOT_FOUND",
                message="Trip not found.",
                details={"trip_id": trip_id},
                http_status=status.HTTP_404_NOT_FOUND,
            )

        seats = Seat.objects.filter(trip=trip).order_by("seat_number")
        data = SeatSerializer(seats, many=True).data

        return Response(
            {"trip_id": trip.id, "items": data},
            status=status.HTTP_200_OK
        )
