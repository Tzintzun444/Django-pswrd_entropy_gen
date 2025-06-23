from django.contrib.auth import get_user_model
from users.models import UserNotVerified
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
        email='email@example.com',
        is_verified=True,
        user_status=False,
        role='customer',
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
            'email': 'email@example.com',
            'password': 'password123',
            'is_verified': True,
            'role': 'customer',
            'is_admin': False
        }
    )
    return user_not_verified


@pytest.fixture
def auth_user(client, general_user):

    client.force_login(general_user)

    return client
