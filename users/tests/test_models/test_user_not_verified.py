from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.utils import IntegrityError
from users.models import UserNotVerified
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_validate_customernotverified_creation():
    now = timezone.now()
    in_5_minutes = now + timezone.timedelta(minutes=5)
    customer_not_verified = UserNotVerified.objects.create(
        email='email@example.com',
        data={
            'username': 'Juan1234',
            'first_name': 'Juan',
            'last_name': 'Lopez',
            'password': 'password1234',
            'role': 'customer',
            'is_verified': True,
            'is_admin': False
        }
    )

    assert customer_not_verified.pk is not None
    assert customer_not_verified.email == 'email@example.com'
    assert customer_not_verified.data['password'] == 'password1234'
    assert customer_not_verified.data['is_verified'] is True
    assert customer_not_verified.data['is_admin'] is False
    assert customer_not_verified.created_at == now
    assert customer_not_verified.expires_at == in_5_minutes


@pytest.mark.django_db
def test_validate_adminnotverified_creation():

    now = timezone.now()
    in_5_minutes = now + timezone.timedelta(minutes=5)
    admin_not_verified = UserNotVerified.objects.create(
        email='email@example.com',
        data={
            'username': 'Juan1234',
            'first_name': 'Juan',
            'last_name': 'Lopez',
            'password': 'password1234',
            'role': 'customer',
            'is_verified': True,
            'is_admin': True
        }
    )

    assert admin_not_verified.pk is not None
    assert admin_not_verified.email == 'email@example.com'
    assert admin_not_verified.data['password'] == 'password1234'
    assert admin_not_verified.data['is_verified'] is True
    assert admin_not_verified.data['is_admin'] is True
    assert admin_not_verified.created_at == now
    assert admin_not_verified.expires_at == in_5_minutes


@pytest.mark.django_db
def test_usernotverified_duplicated_raises_error():

    UserNotVerified.objects.create(
        email='email@example.com',
        data={
            'username': 'Juan1234',
            'first_name': 'Juan',
            'last_name': 'Lopez',
            'password': 'password1234',
            'role': 'customer',
            'is_verified': True,
            'is_admin': False
        }
    )

    with pytest.raises(IntegrityError):
        UserNotVerified.objects.create(
            email='email@example.com',
            data={
                'username': 'Juan1234',
                'first_name': 'Juan',
                'last_name': 'Lopez',
                'password': 'password1234',
                'role': 'customer',
                'is_verified': True,
                'is_admin': False
            }
        )


@pytest.mark.django_db
def test_usernotverified_creates_code_correctly():
    user = UserNotVerified.objects.create(
        email='email@example.com',
        data={
            'username': 'Juan1234',
            'first_name': 'Juan',
            'last_name': 'Lopez',
            'password': 'password1234',
            'role': 'customer',
            'is_verified': True,
            'is_admin': False
        }
    )

    assert isinstance(user.code, str) is True
    assert len(user.code) == 6
    assert int(user.code) > 0
