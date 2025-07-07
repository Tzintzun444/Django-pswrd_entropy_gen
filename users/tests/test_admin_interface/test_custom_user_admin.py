from users.models import CustomUser
from users.admin import CustomUserAdmin
from django.contrib import admin


def test_custom_user_registered_in_admin_interface():

    assert CustomUser in admin.site._registry
    assert isinstance(admin.site._registry[CustomUser], CustomUserAdmin) is True


def test_custom_user_admin_interface_list_display():

    list_display = CustomUserAdmin.list_display

    assert 'username' in list_display
    assert 'email' in list_display
    assert 'role' in list_display
    assert 'user_status' in list_display
    assert 'last_login' in list_display


def test_custom_user_admin_interface_search_fields():

    search_fields = CustomUserAdmin.search_fields

    assert 'username' in search_fields
    assert 'email' in search_fields
    assert 'role' in search_fields
    assert 'date_joined' in search_fields
