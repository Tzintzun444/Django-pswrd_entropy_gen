from users.tests.conftest import auth_user
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_create_password_view_redirects_not_auth_users(client):

    response = client.get(reverse('generator'))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('generator')


@pytest.mark.django_db
def test_create_password_view_renders_correctly(auth_user):

    response = auth_user.get(reverse('generator'))

    assert response.status_code == 200
    assert 'generator.html' in [t.name for t in response.templates]
    assert 'form' in response.context


default_data = {
        'length_password': 12,
        'use_uppercase_letters': True,
        'use_digits': True,
        'use_punctuation_characters': True,
        'custom_characters_allowed': '',
        'characters_not_allowed': ''
    }


@pytest.mark.django_db
def test_create_password_view_session_works(auth_user):

    session = auth_user.session
    session['password'] = 'password123'
    session['password_is_new'] = True
    session.save()

    response = auth_user.get(reverse('generator'))
    new_session = response.wsgi_request.session

    assert 'password' in new_session
    assert 'password' in response.context
    assert 'password_is_new' in new_session
    assert new_session['password_is_new'] is False

    second_response = auth_user.get(reverse('generator'))
    new_session = second_response.wsgi_request.session

    assert 'password' not in new_session
    assert 'password' not in second_response.context
    assert new_session['password_is_new'] is False


@pytest.mark.django_db
def test_create_password_view_generates_passwords(auth_user):

    response = auth_user.post(reverse('generator'), data=default_data)

    assert response.status_code == 302
    assert response.url == reverse('generator')

    session = response.wsgi_request.session

    assert 'password' in session
    assert isinstance(session['password'], str) is True
    assert session['password_is_new'] is True
