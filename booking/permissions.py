from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['manager', 'admin']
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='employee'

class CanApproveBooking(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.groups.filter(name='employee').exists()
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.groups.filter(name__in=['manager', 'admin']).exists()
        return True