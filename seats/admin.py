from django.contrib import admin
from .models import Seat


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "trip", "seat_number", "status")
    list_filter = ("status", "trip")
    search_fields = ("seat_number",)
