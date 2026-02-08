from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "trip", "status", "created_at", "cancelled_at")
    list_filter = ("status", "trip")
    search_fields = ("user__phone",)
