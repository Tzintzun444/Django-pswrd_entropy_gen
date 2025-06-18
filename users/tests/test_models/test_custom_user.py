from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.utils import IntegrityError
from users.models import UserNotVerified
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_validate_customer_creation():
    now = timezone.now()
    customer = User.objects.create(
        username='Juan1234',
        first_name='Juan',
        last_name='Lopez',
        email='fakeemail@example.com',
        role='customer',
        is_verified=True,
        is_staff=False,
        is_superuser=False
    )

    customer.set_password('contraseña1234')

    assert customer.pk is not None
    assert customer.check_password('contraseña1234') is True
    assert customer.email == 'fakeemail@example.com'
    assert customer.is_active is True
    assert customer.is_staff is False
    assert customer.is_superuser is False
    assert customer.registration_date == now


@pytest.mark.django_db
def test_validate_admin_creation():
    now = timezone.now()
    admin = User.objects.create(
        username='administrador234',
        first_name='Jose',
        last_name='Diaz',
        email='newemail@example.com',
        role='admin',
        is_verified=True,
        is_staff=True,
        is_superuser=True,
    )

    admin.set_password('admin1233')

    assert admin.pk is not None
    assert admin.is_active is True
    assert admin.check_password('admin1233')
    assert admin.email == 'newemail@example.com'
    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.registration_date == now


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
def test_user_duplicated_raises_error():
    User.objects.create(
        username='Juan1234',
        first_name='Juan',
        last_name='Lopez',
        email='fakeemail@example.com',
        role='customer',
        is_verified=True,
    )

    with pytest.raises(IntegrityError):
        User(
            username='Juan1234',
            first_name='Lucas',
            last_name='Walker',
            email='fakeemail@example.com',
            role='admin',
            is_verified=False,
        ).save()


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
