from django.contrib import admin
from .models import Car, Booking, Driver

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display =("department", "destination", "status")

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
admin.site.register(Car)
admin.site.register(Driver)