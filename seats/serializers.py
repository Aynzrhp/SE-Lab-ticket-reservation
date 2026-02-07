from rest_framework import serializers
from .models import Seat


class SeatSerializer(serializers.ModelSerializer):
    seat_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Seat
        fields = ("seat_id", "seat_number", "status")
