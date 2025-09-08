from rest_framework import serializers
from .models import Car, Driver, Booking

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    requested_by = serializers.ReadOnlyField(source='requested_by.username')

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status', 'requested_by', 'created_at',  'updated_at']