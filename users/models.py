from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    user_status = models.BooleanField(default=True)  # Activo/Inactivo
    role = models.CharField(
        max_length=10,
        choices=[("customer", "Customer"), ("admin", "Administrator")],
        default="admin"
    )

    def __str__(self):
        return f"{self.username} - ({self.role})"
