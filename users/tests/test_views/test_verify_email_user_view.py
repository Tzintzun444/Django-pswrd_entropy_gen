from django.urls import reverse
from django.contrib.auth import get_user_model
from users.tests.conftest import user_not_verified, auth_user, admin_user, general_user
from users.models import UserNotVerified
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_auth_user_is_redirected(auth_user):

    response = auth_user.get(reverse('verify_email'))

    assert response.status_code == 302
    assert response.url == reverse('index')


@pytest.mark.django_db
def test_verify_email_user_renders_correctly(client):

    session = client.session
    session['verification_email'] = 'correo@example.com'
    session.save()
    response = client.get(reverse('verify_email'))

    assert response.status_code == 200
    assert 'verify_email.html' in [t.name for t in response.templates]
    assert 'form' in response.context
    assert 'email' in response.context
    assert 'resend_blocked' in response.context
    assert 'cooldown_remaining' in response.context


@pytest.mark.django_db
def test_auth_admin_user_is_not_redirected(client, admin_user):

    client.force_login(admin_user)
    response = client.get(reverse('verify_email'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_code_shows_error(client, user_not_verified):

    session = client.session
    session['verification_email'] = 'email@example.com'
    session.save()

    data = {
        'code': 'invalid'
    }
    response = client.post(reverse('verify_email'), data=data)

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'code' in response.context['form'].errors


@pytest.mark.django_db
def test_verify_email_user_works(client, user_not_verified):
    email = 'email@example.com'
    session = client.session
    session['verification_email'] = email
    session.save()
    code = user_not_verified.code

    data = {}

    for index in range(6):
        data[f'code_{index}'] = code[index]

    response = client.post(reverse('verify_email'), data=data)

    assert UserNotVerified.objects.filter(code=code).exists() is False
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert User.objects.filter(email=email).exists() is True
    assert client.session.get('verification_email', None) is None
