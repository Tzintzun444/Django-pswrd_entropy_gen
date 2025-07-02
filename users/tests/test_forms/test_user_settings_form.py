from users.forms import UserSettingsForm
from users.tests.conftest import general_user
from django.contrib.auth import get_user_model
import pytest

data = {
        'username': 'user_test',
        'first_name': 'new_name',
        'last_name': 'last_name',
        'password': 'new_password',
        'confirm_password': 'new_password'
    }


@pytest.mark.django_db
def test_user_settings_form_with_valid_data(general_user):

    form = UserSettingsForm(data=data, instance=general_user)

    assert form.is_valid() is True
    assert 'username' in form.fields
    assert 'first_name' in form.fields
    assert 'last_name' in form.fields
    assert 'email' in form.fields
    assert 'password' in form.fields
    assert 'confirm_password' in form.fields


@pytest.mark.django_db
def test_user_settings_form_username_already_exists_error(general_user):
    UserModel = get_user_model()
    user = UserModel(
        username='new_user_test',
        first_name='first_name',
        last_name='last_name',
        email='newemail@example.com',
        is_verified=True,
        user_status=False,
        role='customer',
        is_staff=True,
        is_superuser=True
    )
    user.set_password('password123')
    user.save()

    data['username'] = user.username
    form = UserSettingsForm(data=data, instance=general_user)

    assert form.is_valid() is False
    assert 'username' in form.errors
    assert 'Username already exists' in form.errors['username']


@pytest.mark.django_db
def test_user_settings_form_length_password_error(general_user):

    data['password'] = '123456'
    data['confirm_password'] = '123456'
    form = UserSettingsForm(data=data)

    assert form.is_valid() is False
    assert 'password' in form.errors
    assert 'At least 8 characters' in form.errors['password']


@pytest.mark.django_db
def test_user_settings_form_numeric_password_error():

    data['password'] = '123456789'
    data['confirm_password'] = '123456789'
    form = UserSettingsForm(data=data)

    assert form.is_valid() is False
    assert 'password' in form.errors
    assert 'Password can\'t be only numeric' in form.errors['password']


@pytest.mark.django_db
def test_user_settings_form_passwords_dont_match_error(general_user):

    data['password'] = 'password1'
    data['confirm_password'] = 'different-password'
    form = UserSettingsForm(data=data)

    assert form.is_valid() is False
    assert 'confirm_password' in form.errors
    assert 'Passwords don\'t match' in form.errors['confirm_password']
