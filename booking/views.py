from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from .models import Booking, Car, Driver
from .serializers import BookingSerializer
from .permissions import IsManagerOrAdmin, IsEmployee
from .serializers import CarSerializer, DriverSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsEmployee]
        elif self.action in ['approve', 'reject']:
            permission_classes = [IsAuthenticated, IsManagerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        serializer.save(
            requested_by=self.request.user,
            department=self.request.user.department
        )

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {"detail": "Only pending bookings can be approved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assign car and driver if provided
        car_id = request.data.get("car")
        driver_id = request.data.get("driver")

        if car_id:
            car = Car.objects.get(id=car_id)
            if not car.is_available:
                return Response({"detail": "Car not available."}, status=status.HTTP_400_BAD_REQUEST)
            booking.car = car
            car.is_available = False
            car.save()

        if driver_id:
            driver = Driver.objects.get(id=driver_id)
            if not driver.is_available:
                return Response({"detail": "Driver not available."}, status=status.HTTP_400_BAD_REQUEST)
            booking.driver = driver
            driver.is_available = False
            driver.save()

        booking.status = Booking.STATUS_APPROVED
        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {"detail": "Only pending bookings can be rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = Booking.STATUS_REJECTED
        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my(self, request):
        qs = Booking.objects.filter(department=request.user.department)
        serializer = BookingSerializer(qs, many=True)
        return Response(serializer.data)
