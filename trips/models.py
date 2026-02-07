from django.db import models


class Trip(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
    )

    origin = models.CharField(max_length=80)
    destination = models.CharField(max_length=80)
    departure_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    # طبق API_SPEC باید خروجی total_seats داشته باشد
    total_seats = models.PositiveIntegerField(default=44)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} -> {self.destination} @ {self.departure_time}"
