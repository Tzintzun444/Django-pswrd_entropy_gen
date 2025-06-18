from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.fixture
def general_user(django_user_model):
    user = User(
        username='user_test',
        first_name='first_name',
        last_name='last_name',
        email='email@example.com',
        is_verified=True,
        role='customer',
    )
    user.set_password('password123')
    user.save()
    return user


@pytest.fixture
def auth_user(client, general_user):

    client.login(username='user_test', password='password123')

    return client
