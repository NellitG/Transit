from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from booking.models import Booking
from .models import Notification

# Notify when a user account is created
@receiver(post_save, sender=User)
def notify_user_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message=f"Welcome {instance.username}! Your account has been created."
        )
# Notify when booking status changes
@receiver(post_save, sender=Booking)
def notify_booking_status_change(sender, instance, created, **kwargs):
    if not created:
        Notification.objects.create(
            user=instance.requested_by,
            message=f"Your booking status has changed to {instance.status}."
        )