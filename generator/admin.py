from django.contrib import admin
from .models import Password


# Register your models here.
@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):

    list_display = ['user__username', 'password', 'entropy', 'decryption_years_needed', 'creation_date']
    search_fields = ['user__username', 'password', 'entropy', 'decryption_years_needed', 'creation_date']
