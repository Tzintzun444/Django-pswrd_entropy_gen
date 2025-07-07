from django.contrib import admin
from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'user_status', 'last_login']
    search_fields = ['username', 'email', 'role', 'date_joined']
