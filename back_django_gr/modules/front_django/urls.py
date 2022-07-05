from django.urls import path
from .views import ReportReservations

app_name = 'guestready_front'
urlpatterns = [
    path('', ReportReservations.as_view()),
]
