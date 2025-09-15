from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message', 'created_at', 'is_read']
        read_only_fields = ['id', 'message', 'created_at']