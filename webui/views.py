from django.views.generic import TemplateView

class LoginPageView(TemplateView):
    template_name = "login.html"

class RegisterPageView(TemplateView):
    template_name = "register.html"

class TripsPageView(TemplateView):
    template_name = "trips.html"

class TripDetailPageView(TemplateView):
    template_name = "trip_detail.html"

class ReservationsPageView(TemplateView):
    template_name = "reservations.html"