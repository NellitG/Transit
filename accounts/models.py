from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_EMPLOYEE = 'employee'
    ROLE_MANAGER = 'manager'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_EMPLOYEE, 'Employee'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_ADMIN, 'Admin'),
    ]

    department = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)

    def is_manager(self):
        return self.role == self.ROLE_MANAGER
    
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
    
    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE