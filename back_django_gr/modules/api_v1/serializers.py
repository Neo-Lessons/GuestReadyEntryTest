from rest_framework import serializers
from modules.core.models.hospitality import reservation as Reservation
from modules.core.models.hospitality import rental as Rental

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    rental = RentalSerializer(read_only=True)
    id_prev = serializers.CharField()

    class Meta:
        model = Reservation
        fields = '__all__'
