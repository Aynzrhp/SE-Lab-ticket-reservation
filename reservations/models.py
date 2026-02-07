from django.db import models
from django.conf import settings
from trips.models import Trip
from seats.models import Seat


class Reservation(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="reservations")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # صندلی‌ها (یک رزرو می‌تواند چند صندلی داشته باشد)
    seats = models.ManyToManyField(Seat, related_name="reservations")

    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reservation {self.id} - {self.user_id} - {self.trip_id} - {self.status}"
