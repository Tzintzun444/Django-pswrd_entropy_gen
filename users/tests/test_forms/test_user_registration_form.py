from users.forms import UserRegistrationForm
from users.tests.conftest import data_for_user_registration_form, general_user
import pytest


@pytest.mark.django_db
def test_user_registration_form_using_valid_data(data_for_user_registration_form):

    form = UserRegistrationForm(data=data_for_user_registration_form)
    fields = form.fields

    assert form.is_valid()
    assert 'username' in fields
    assert 'first_name' in fields
    assert 'last_name' in fields
    assert 'email' in fields
    assert 'password' in fields
    assert 'confirm_password' in fields
    assert 'is_admin' in fields

    user_not_verified_instance = form.save()

    assert user_not_verified_instance.pk is not None
    assert user_not_verified_instance.email == data_for_user_registration_form['email']
    assert user_not_verified_instance.data == {
        'username': data_for_user_registration_form['username'],
        'first_name': data_for_user_registration_form['first_name'],
        'last_name': data_for_user_registration_form['last_name'],
        'password': data_for_user_registration_form['password'],
        'is_admin': data_for_user_registration_form['is_admin']
    }


@pytest.mark.django_db
def test_user_registration_form_with_commit_false(data_for_user_registration_form):

    form = UserRegistrationForm(data=data_for_user_registration_form)

    assert form.is_valid() is True

    instance = form.save(commit=False)

    assert instance.pk is None


@pytest.mark.django_db
def test_user_registration_form_username_already_exists_error(general_user, data_for_user_registration_form):

    form = UserRegistrationForm(data=data_for_user_registration_form)

    assert form.is_valid() is False
    assert 'username' in form.errors
    assert 'Username already exists' in form.errors['username']


@pytest.mark.django_db
def test_user_registration_form_email_already_in_use_error(general_user, data_for_user_registration_form):

    form = UserRegistrationForm(data=data_for_user_registration_form)

    assert form.is_valid() is False
    assert 'email' in form.errors
    assert 'Email already in use' in form.errors['email']


@pytest.mark.django_db
def test_user_registration_form_password_is_numeric_error(data_for_user_registration_form):

    data_for_user_registration_form['password'] = '12345566'
    form = UserRegistrationForm(data=data_for_user_registration_form)

    assert form.is_valid() is False
    assert 'password' in form.errors
    assert 'Password can\'t be only numeric' in form.errors['password']


@pytest.mark.django_db
def test_user_registration_form_passwords_dont_match_error(data_for_user_registration_form):

    data_for_user_registration_form['confirm_password'] = 'differentPassword123'
    form = UserRegistrationForm(data=data_for_user_registration_form)

    assert form.is_valid() is False
    assert 'confirm_password' in form.errors
    assert 'Passwords don\'t match' in form.errors['confirm_password']
