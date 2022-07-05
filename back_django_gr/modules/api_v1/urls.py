from django.urls import path
from .views import ReservationsCreateListView

app_name = 'api_v1'
urlpatterns = [
    path('', ReservationsCreateListView.as_view()),
]
