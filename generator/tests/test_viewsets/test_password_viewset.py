from generator.viewsets import PasswordViewSet
from generator.serializers import PasswordGenerationSerializer, PasswordModelSerializer
from generator.permissions import PasswordPermission
from generator.models import Password
from users.tests.conftest import api_client_auth_with_general_user
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APIClient
import pytest

factory = APIRequestFactory()


def test_password_viewset_attributes():

    viewset = PasswordViewSet()

    assert viewset.serializer_class == PasswordGenerationSerializer
    assert viewset.permission_classes == [PasswordPermission]


@pytest.mark.parametrize('action,serializer_class',[
    ('list', PasswordModelSerializer),
    ('retrieve', PasswordModelSerializer),
    ('create', PasswordGenerationSerializer),
    ('destroy', PasswordModelSerializer),
    ('other', PasswordModelSerializer)
])
@pytest.mark.django_db
def test_password_viewset_get_serializer_class_method(action, serializer_class):

    viewset = PasswordViewSet()
    viewset.action = action

    assert viewset.get_serializer_class() == serializer_class


@pytest.mark.django_db
def test_password_viewset_list_action(general_password, api_client_auth_with_general_user, general_user):

    response = api_client_auth_with_general_user.get(reverse('password-list'))

    assert response.status_code == 200
    assert len(response.data) == len(Password.objects.filter(user=general_user))

@pytest.mark.django_db
def test_password_viewset_list_action_with_not_auth_user():

    client = APIClient()
    response = client.get(reverse('password-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_password_viewset_retrieve_action(general_password, api_client_auth_with_general_user, general_user):

    response = api_client_auth_with_general_user.get(reverse('password-detail', args=[general_password.pk]))

    assert response.status_code == 200
    assert response.data['id'] == general_password.pk
    assert response.data['user'] == general_password.user.pk
    assert response.data['password'] == general_password.password


@pytest.mark.django_db
def test_password_viewset_retrieve_action_with_not_auth_user(general_password, general_user):

    client = APIClient()
    response = client.get(reverse('password-detail', args=[general_password.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_password_viewset_retrieve_action_with_not_auth_user(api_client_auth_with_general_user, general_user):

    User = get_user_model()
    user = User(
        username='user_test1',
        first_name='first_name',
        last_name='last_name',
        email='email1@example.com',
        is_verified=True,
        user_status=False,
        role='customer',
    )
    user.set_password('password123')
    user.save()

    password = Password.objects.create(
        user=user,
        password='fake_password',
        entropy=77,
        decryption_years_needed=17000
    )

    response = api_client_auth_with_general_user.get(reverse('password-detail', args=[password.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_password_viewset_create_action(api_client_auth_with_general_user, general_user):

    data = {
        'length': 12,
        'use_uppercase': True,
        'use_numbers': True,
        'use_punctuations': True,
        'custom_characters': '',
        'characters_not_allowed': ''
    }

    response = api_client_auth_with_general_user.post(reverse('password-list'), data=data)
    password = Password.objects.filter(user=general_user)

    assert response.status_code == 201
    assert password.exists() is True
    assert response.data['user'] == general_user.pk
    assert response.data['password'] == password.first().password


@pytest.mark.django_db
def test_password_viewset_create_action_with_not_auth_user(general_user):

    data = {
        'length': 12,
        'use_uppercase': True,
        'use_numbers': True,
        'use_punctuations': True,
        'custom_characters': '',
        'characters_not_allowed': ''
    }
    client = APIClient()
    response = client.post(reverse('password-list'), data=data)
    password = Password.objects.filter(user=general_user)

    assert response.status_code == 403
    assert password.exists() is False


@pytest.mark.django_db
def test_password_viewset_destroy_action(general_password, general_user, api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.delete(reverse('password-detail', args=[general_password.pk]))

    assert response.status_code == 204
    assert Password.objects.filter(pk=general_password.pk).exists() is False


@pytest.mark.django_db
def test_password_viewset_destroy_action_with_not_auth_user(general_password):

    client = APIClient()
    response = client.delete(reverse('password-detail', args=[general_password.pk]))

    assert response.status_code == 404
    assert Password.objects.filter(pk=general_password.pk).exists() is True


@pytest.mark.django_db
def test_password_viewset_update_action_returns_405(
        api_client_auth_with_general_user, data_for_general_password, general_password):

    response = api_client_auth_with_general_user.post(
        reverse('password-detail', args=[general_password.pk]), data=data_for_general_password
    )

    assert response.status_code == 405
