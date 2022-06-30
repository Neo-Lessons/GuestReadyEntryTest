from django.shortcuts import render
from django.views.generic import View
from modules.core.models import reservation

class ReportReservations(View):
    def get(self, request):
        dataSET = reservation.objects.selectReservationWithLast()

        context = {
            'dataSET': dataSET,
        }

        return render(request, 'index.html', context)