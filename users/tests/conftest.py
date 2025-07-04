from django.contrib.auth import get_user_model
from users.models import UserNotVerified
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def general_user():
    user = User(
        username='user_test',
        first_name='first_name',
        last_name='last_name',
        email='email@example.com',
        is_verified=True,
        user_status=False,
        role='customer',
    )
    user.set_password('password123')
    user.save()
    return user


@pytest.fixture
def admin_user():
    user = User(
        username='user_admin_test',
        first_name='first_name',
        last_name='last_name',
        email='admin@example.com',
        is_verified=True,
        user_status=False,
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    user.set_password('password123')
    user.save()
    return user


@pytest.fixture
def user_not_verified():

    user_not_verified = UserNotVerified.objects.create(
        email='email@example.com',
        data={
            'username': 'user_test',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': 'password123',
            'is_admin': False
        }
    )
    return user_not_verified


@pytest.fixture
def auth_user(client, general_user):

    client.force_login(general_user)

    return client


@pytest.fixture
def data_for_user_registration_form():

    data = {
        'username': 'user_test',
        'first_name': 'user',
        'last_name': 'test',
        'email': 'email@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'is_admin': False
    }

    return data


@pytest.fixture()
def api_client_auth_with_admin(admin_user):

    client = APIClient()
    client.force_authenticate(user=admin_user)

    return client


@pytest.fixture()
def api_client_auth_with_general_user(general_user):

    client = APIClient()
    client.force_authenticate(user=general_user)

    return client