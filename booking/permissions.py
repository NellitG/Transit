from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and (user.role == 'MANAGER' or user.role == 'ADMIN'))
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.role == 'EMPLOYEE')
    
class IsOwnerOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == ['MANAGER', 'ADMIN']:
            return True
        return obj.requested_by == user
