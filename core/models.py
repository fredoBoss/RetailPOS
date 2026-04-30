from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    CASHIER = 'cashier'

    ROLE_CHOICES = [
        (SUPERADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (CASHIER, 'Cashier'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CASHIER)

    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"
