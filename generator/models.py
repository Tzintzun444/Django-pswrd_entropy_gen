from django.db import models
from users.models import CustomUser


class Password(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='passwords')
    password = models.CharField(max_length=30)
    entropy = models.DecimalField(max_digits=10, decimal_places=2)
    decryption_years_needed = models.DecimalField(max_digits=50, decimal_places=3)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.password}'
