from django.urls import path
from .views import ReservationsRootView, ReservationItemView

urlpatterns = [
    path("reservations", ReservationsRootView.as_view(), name="reservations-root"),
    path("reservations/<int:reservation_id>", ReservationItemView.as_view(), name="reservations-item"),
]
