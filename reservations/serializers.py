from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(source="id", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    trip_id = serializers.IntegerField(source="trip.id", read_only=True)
    seat_ids = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            "reservation_id",
            "user_id",
            "trip_id",
            "status",
            "seat_ids",
            "created_at",
            "cancelled_at",
        )

    def get_seat_ids(self, obj: Reservation):
        return list(obj.seats.values_list("id", flat=True))


class CreateReservationSerializer(serializers.Serializer):
    trip_id = serializers.IntegerField()
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class CancelReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
