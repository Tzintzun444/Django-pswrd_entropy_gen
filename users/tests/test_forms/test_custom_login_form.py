from users.forms import CustomLoginForm
from users.tests.conftest import general_user
import pytest


@pytest.mark.django_db
def test_custom_login_form_with_valid_data(general_user):

    data = {
        'username': general_user.username,
        'password': 'password123'
    }
    form = CustomLoginForm(data=data)

    assert form.is_valid() is True
    assert 'username' in form.fields
    assert 'password' in form.fields


@pytest.mark.django_db
def test_custom_login_form_invalid_username_error(general_user):

    data = {
        'username': 'unknown_user',
        'password': 'password123'
    }
    form = CustomLoginForm(data=data)

    assert form.is_valid() is False
    assert '__all__' in form.errors
    assert 'Invalid data, please try again' in form.errors['__all__']


@pytest.mark.django_db
def test_custom_login_form_invalid_password_error(general_user):

    data = {
        'username': general_user.username,
        'password': 'invalid-password'
    }
    form = CustomLoginForm(data=data)

    assert form.is_valid() is False
    assert '__all__' in form.errors
    assert 'Invalid data, please try again' in form.errors['__all__']


@pytest.mark.django_db
def test_custom_login_form_inactive_user_error(general_user):

    general_user.is_active = False
    general_user.save()
    data = {
        'username': general_user.username,
        'password': 'password123'
    }

    form = CustomLoginForm(data=data)

    assert form.is_valid() is False
    assert 'inactive' in form.error_messages
    assert '__all__' in form.errors
    assert 'Invalid data, please try again' in form.errors['__all__']
