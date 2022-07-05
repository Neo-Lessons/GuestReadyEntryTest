from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from modules.core.models.hospitality import reservation as Reservation
from .serializers import ReservationSerializer


class ReservationsCreateListView(GenericAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.selectReservationWithLast()

    def get(self, request):
        reservations = self.get_queryset()
        serializer = self.serializer_class(reservations, many=True)
        return Response(serializer.data)