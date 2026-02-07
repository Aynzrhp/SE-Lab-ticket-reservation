from django.urls import path
from .views import TripListView, TripDetailView

urlpatterns = [
    path("trips", TripListView.as_view(), name="trips-list"),
    path("trips/<int:pk>", TripDetailView.as_view(), name="trips-detail"),
]
