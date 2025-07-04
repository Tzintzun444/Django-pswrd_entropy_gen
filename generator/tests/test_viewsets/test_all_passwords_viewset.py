from generator.serializers import PasswordModelSerializer
from generator.viewsets import AllPasswordsViewSet
from generator.models import Password
from users.permissions import IsStaffOrAdmin
from users.tests.conftest import admin_user, api_client_auth_with_admin
from django.urls import reverse
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_all_passwords_viewset_attributes():

    viewset = AllPasswordsViewSet()

    assert viewset.serializer_class == PasswordModelSerializer
    assert viewset.permission_classes == [IsStaffOrAdmin]


@pytest.mark.django_db
def test_all_passwords_viewset_list_action(api_client_auth_with_admin, admin_user):

    password = Password.objects.create(
        user=admin_user,
        password='fake_password',
        entropy=77,
        decryption_years_needed=17000
    )
    response = api_client_auth_with_admin.get(reverse('all_passwords-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == len(Password.objects.filter(user=admin_user))


@pytest.mark.django_db
def test_all_passwords_viewset_retrieve_action(api_client_auth_with_admin, admin_user):

    password = Password.objects.create(
        user=admin_user,
        password='fake_password',
        entropy=77,
        decryption_years_needed=17000
    )
    response = api_client_auth_with_admin.get(reverse('all_passwords-detail', args=[password.pk]))

    assert response.status_code == 200
    assert response.data['id'] == password.pk
    assert response.data['user'] == password.user.pk
    assert response.data['password'] == password.password


@pytest.mark.django_db
def test_all_passwords_viewset_not_allowed_method(api_client_auth_with_admin, admin_user):

    data = {'password': 'password123'}
    response = api_client_auth_with_admin.post(reverse('all_passwords-list'), data=data)

    assert response.status_code == 405


@pytest.mark.django_db
def test_all_passwords_viewset_permissions():

    client = APIClient()
    response = client.get(reverse('all_passwords-list'))

    assert response.status_code == 403
