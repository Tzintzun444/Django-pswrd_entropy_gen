from users.serializers import CustomCustomerSerializer
from users.tests.conftest import general_user
from django.contrib.auth import get_user_model
import pytest

data = {
    'username': 'user_test',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'password': 'password123',
    'email': 'email@example.com'
}

User = get_user_model()


@pytest.mark.django_db
def test_custom_customer_serializer_with_valid_data():

    serializer = CustomCustomerSerializer(data=data)
    assert serializer.is_valid() is True

    fields = serializer.fields
    assert 'username' in fields
    assert 'first_name' in fields
    assert 'last_name' in fields
    assert 'email' in fields
    assert 'password' in fields
    assert 'passwords' in fields

    validated_data = serializer.validated_data
    assert 'passwords' not in validated_data

    assert 'user_test' == validated_data['username']
    assert 'first_name' == validated_data['first_name']
    assert 'last_name' == validated_data['last_name']
    assert 'email@example.com' == validated_data['email']
    assert 'password123' == validated_data['password']

    instance = serializer.save()
    instance.set_password(instance.password)

    assert instance.pk is not None
    assert instance.username == 'user_test'
    assert instance.email == 'email@example.com'
    assert instance.check_password('password123') is True


@pytest.mark.django_db
def test_custom_customer_serializer_with_invalid_data():

    data['password'] = '123456'

    serializer = CustomCustomerSerializer(data=data)
    assert serializer.is_valid() is False


@pytest.mark.django_db
def test_custom_customer_serializer_length_password_error():

    data['password'] = '123456'
    serializer = CustomCustomerSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'password' == str(serializer.errors['non_field_errors'][0])
    assert 'Password must have at least 8 characters' == serializer.errors['non_field_errors'][0].code


@pytest.mark.django_db
def test_custom_customer_serializer_password_is_digit_error():

    data['password'] = '1234567890'
    serializer = CustomCustomerSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'password' in str(serializer.errors['non_field_errors'][0])
    assert 'Password can\'t be only numeric' == serializer.errors['non_field_errors'][0].code


@pytest.mark.django_db
def test_custom_customer_serializer_username_already_exists(general_user):

    serializer = CustomCustomerSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'username' in serializer.errors
    assert 'A user with that username already exists.' == str(serializer.errors['username'][0])


@pytest.mark.django_db
def test_custom_customer_serializer_email_already_exists(general_user):

    data['username'] = 'new_username'
    serializer = CustomCustomerSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'email' in serializer.errors
    assert 'user with this email already exists.' == str(serializer.errors['email'][0])


@pytest.mark.django_db
def test_custom_customer_serializer_update_method(general_user):

    data['username'] = 'new_username'
    data['password'] = 'new_password'

    serializer = CustomCustomerSerializer(data=data, instance=general_user)
    assert serializer.is_valid() is True

    instance = serializer.save()

    assert instance.username == 'new_username'
    assert instance.check_password('new_password') is True


@pytest.mark.django_db
def test_custom_customer_serializer_username_already_exists_in_update(general_user):

    new_user = User.objects.create(
        username='new_username',
        first_name='first_name',
        last_name='last_name',
        email='new_email@example.com',
        password='password',
        role='customer',
        is_verified=True
    )

    data['username'] = new_user.username
    serializer = CustomCustomerSerializer(data=data, instance=general_user)

    assert serializer.is_valid() is False
    assert 'username' in serializer.errors
    assert 'A user with that username already exists.' == str(serializer.errors['username'][0])


@pytest.mark.django_db
def test_custom_customer_serializer_email_already_exists_in_update(general_user):

    new_user = User.objects.create(
        username='new_username',
        first_name='first_name',
        last_name='last_name',
        email='new_email@example.com',
        password='password',
        role='customer',
        is_verified=True
    )

    data['email'] = new_user.email
    serializer = CustomCustomerSerializer(data=data, instance=general_user)

    assert serializer.is_valid() is False
    assert 'email' in serializer.errors
    assert 'user with this email already exists.' == str(serializer.errors['email'][0])


@pytest.mark.django_db
def test_custom_customer_serializer_length_password_error_in_update(general_user):

    data['password'] = '123456'
    serializer = CustomCustomerSerializer(data=data, instance=general_user)

    assert serializer.is_valid() is False
    assert 'password' == str(serializer.errors['non_field_errors'][0])
    assert 'Password must have at least 8 characters' == serializer.errors['non_field_errors'][0].code


@pytest.mark.django_db
def test_custom_customer_serializer_password_is_digit_error_in_update(general_user):

    data['password'] = '1234567890'
    serializer = CustomCustomerSerializer(data=data, instance=general_user)

    assert serializer.is_valid() is False
    assert 'password' in str(serializer.errors['non_field_errors'][0])
    assert 'Password can\'t be only numeric' == serializer.errors['non_field_errors'][0].code
