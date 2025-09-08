from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from .views import CarViewSet, DriverViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='car')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]