from django.db.models.signals import post_save
from django.dispatch import receiver
from trips.models import Trip
from .models import Seat


@receiver(post_save, sender=Trip)
def create_seats_for_trip(sender, instance: Trip, created, **kwargs):
    if not created:
        return

    if instance.seats.exists():
        return

    total = instance.total_seats or 0
    seats = [
        Seat(trip=instance, seat_number=str(i), status="available")
        for i in range(1, total + 1)
    ]
    Seat.objects.bulk_create(seats)
