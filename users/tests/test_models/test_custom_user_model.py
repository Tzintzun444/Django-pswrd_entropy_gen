from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.utils import IntegrityError
from freezegun import freeze_time
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_validate_customer_creation():
    with freeze_time("2025-01-01 00:00:00"):
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
    assert customer.date_joined == now


@pytest.mark.django_db
def test_validate_admin_creation():
    with freeze_time("2025-01-01 00:00:00"):
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
    assert admin.date_joined == now


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
