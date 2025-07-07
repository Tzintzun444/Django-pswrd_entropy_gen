from generator.models import Password
from generator.admin import PasswordAdmin
from django.contrib import admin


def test_password_registered_in_admin_interface():

    assert Password in admin.site._registry
    assert isinstance(admin.site._registry[Password], PasswordAdmin)


def test_password_admin_interface_list_display():

    list_display = PasswordAdmin.list_display

    assert 'user__username' in list_display
    assert 'password' in list_display
    assert 'entropy' in list_display
    assert 'decryption_years_needed' in list_display
    assert 'creation_date' in list_display


def test_password_admin_interface_search_fields():

    search_fields = PasswordAdmin.search_fields

    assert 'user__username' in search_fields
    assert 'password' in search_fields
    assert 'entropy' in search_fields
    assert 'decryption_years_needed' in search_fields
    assert 'creation_date' in search_fields
