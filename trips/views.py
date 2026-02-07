from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import make_aware

from .models import Trip
from .serializers import TripSerializer
from .pagination import StandardPagination


def error_response(code: str, message: str, details=None, http_status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            }
        },
        status=http_status,
    )


class TripListView(generics.ListAPIView):
    serializer_class = TripSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = Trip.objects.all().order_by("departure_time")

        origin = self.request.query_params.get("origin")
        destination = self.request.query_params.get("destination")
        date_str = self.request.query_params.get("date")

        if origin:
            qs = qs.filter(origin__icontains=origin.strip())

        if destination:
            qs = qs.filter(destination__icontains=destination.strip())

        if date_str:
            # انتظار: YYYY-MM-DD
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                qs = qs.filter(departure_time__date=d)
            except ValueError:
                # خطا را در list برمی‌گردانیم
                self._date_error = True

        return qs

    def list(self, request, *args, **kwargs):
        # اگر date فرمت غلط باشد:
        if getattr(self, "_date_error", False):
            return error_response(
                code="VALIDATION_ERROR",
                message="Invalid date format. Use YYYY-MM-DD.",
                details={"date": request.query_params.get("date")},
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "page": self.paginator.page.number,
                    "page_size": self.paginator.get_page_size(self.request),
                    "total": self.paginator.page.paginator.count,
                },
                "items": data,
            },
            status=200,
        )


class TripDetailView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        trip = self.get_object()
        data = self.get_serializer(trip).data
        return Response({"trip": data}, status=200)
