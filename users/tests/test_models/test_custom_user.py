from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_validate_customer_creation():
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
    assert customer.is_active is True
    assert customer.is_staff is False
    assert customer.is_superuser is False


@pytest.mark.django_db
def test_validate_admin_creation():
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
    assert admin.is_staff is True
    assert admin.is_superuser is True
