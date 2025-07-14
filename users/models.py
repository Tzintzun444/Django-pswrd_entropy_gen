from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    user_status = models.BooleanField(default=False)
    role = models.CharField(
        max_length=10,
        choices=[("customer", "Customer"), ("admin", "Administrator")],
        default="admin"
    )

    def __str__(self):
        return f"{self.username} - ({self.role})"


class UserNotVerified(models.Model):

    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    data = models.JSONField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def reset_code(self):

        self.code = self.generate_code()
        self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

    @classmethod
    def generate_code(cls):
        return str(secrets.randbelow(999999)).zfill(6)
