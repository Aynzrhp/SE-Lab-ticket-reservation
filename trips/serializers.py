from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    trip_id = serializers.IntegerField(source="id", read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            "trip_id",
            "origin",
            "destination",
            "departure_time",
            "price",
            "status",
            "total_seats",
            "available_seats",
        )

    def get_available_seats(self, obj: Trip) -> int:
        try:
            return obj.seats.filter(status="available").count()
        except Exception:
            return obj.total_seats
