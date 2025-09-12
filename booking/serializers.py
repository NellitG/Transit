from rest_framework import serializers
from .models import Car, Driver, Booking
from rest_framework.exceptions import ValidationError

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_superuser:
            raise serializers.ValidationError("Superusers cannot create bookings.")    

        validated_data['status'] = 'pending'
        validated_data['created_by'] = user
        return super().create(validated_data)