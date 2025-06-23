from django.urls import reverse
from users.tests.conftest import auth_user, admin_user
from users.models import UserNotVerified
from unittest.mock import patch
import pytest


def test_sign_up_user_view_renders_correctly(client):

    response = client.get(reverse('sign_up'))

    assert response.status_code == 200
    assert 'registrate_client.html' in [t.name for t in response.templates]
    assert 'form' in response.context


@pytest.mark.django_db
def test_sign_up_user_view_redirects_auth_users(auth_user):

    response = auth_user.get(reverse('sign_up'))

    assert response.status_code == 302
    assert response.url == reverse('index')


@pytest.mark.django_db
def test_sign_up_user_view_allows_auth_admin_users(client, admin_user):

    client.force_login(admin_user)

    response = client.get(reverse('sign_up'))

    assert response.status_code == 200
    assert 'registrate_client.html' in [t.name for t in response.templates]
    assert 'form' in response.context


@pytest.mark.django_db
@patch('users.views.send_mail')
def test_sign_up_user_view_success(mock_send_mail, client):

    data = {
        'username': 'test_user',
        'first_name': 'User',
        'last_name': 'Test',
        'email': 'email@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'is_admin': False
    }

    response = client.post(reverse('sign_up'), data=data)

    assert response.status_code == 302
    assert response.url == reverse('verify_email')
    assert UserNotVerified.objects.filter(email='email@example.com').exists() is True

    verification = UserNotVerified.objects.get(email='email@example.com')
    assert verification.data['username'] == 'test_user'
    assert verification.data['password'] == 'password123'
    assert verification.data['is_admin'] is False
    assert 'email' not in verification.data

    session = client.session

    assert 'verification_email' in session
    assert session['verification_email'] == 'email@example.com'

    mock_send_mail.assert_called_once()
    args, kwargs = mock_send_mail.call_args
    assert args[0] == 'Email verification'
    assert 'Your verification code is' in args[1]
    assert args[2] == 'pswrdentropygen@gmail.com'
    assert args[3] == ['email@example.com']
    assert not kwargs.get('fail_silently', True)
