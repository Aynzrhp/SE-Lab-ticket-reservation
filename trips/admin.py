from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "departure_time", "price", "status", "total_seats")
    list_filter = ("status", "origin", "destination")
    search_fields = ("origin", "destination")
