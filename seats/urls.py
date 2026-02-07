from django.urls import path
from .views import TripSeatMapView

urlpatterns = [
    path("trips/<int:trip_id>/seats", TripSeatMapView.as_view(), name="trip-seats"),
]
