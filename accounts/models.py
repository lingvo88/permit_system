from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model supporting both customers and employees."""
    
    class UserType(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        EMPLOYEE = 'employee', 'Employee'
        ADMIN = 'admin', 'Admin'
    
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    phone = models.CharField(max_length=20, blank=True)
    
    # For customers - linked to their company
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users'
    )
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"
    
    @property
    def is_customer(self):
        return self.user_type == self.UserType.CUSTOMER
    
    @property
    def is_employee(self):
        return self.user_type in [self.UserType.EMPLOYEE, self.UserType.ADMIN]
    
    @property
    def is_admin_user(self):
        return self.user_type == self.UserType.ADMIN

