from django.urls import path
from .views import (
    LoginPageView,
    RegisterPageView,
    TripsPageView,
    TripDetailPageView,
    ReservationsPageView,
)

urlpatterns = [
    path("", TripsPageView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login-page"),
    path("register/", RegisterPageView.as_view(), name="register-page"),
    path("trips/", TripsPageView.as_view(), name="trips-page"),
    path("trips/<int:trip_id>/", TripDetailPageView.as_view(), name="trip-detail-page"),
    path("reservations/", ReservationsPageView.as_view(), name="reservations-page"),
]