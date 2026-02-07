from django.db import models
from trips.models import Trip


class Seat(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("reserved", "Reserved"),
    )

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5)  # مطابق API_SPEC به صورت string
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["trip", "seat_number"], name="uniq_seat_per_trip")
        ]
        ordering = ["trip_id", "seat_number"]

    def __str__(self):
        return f"Trip {self.trip_id} - Seat {self.seat_number} ({self.status})"
