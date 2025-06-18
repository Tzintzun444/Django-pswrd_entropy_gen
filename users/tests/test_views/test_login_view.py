from django.urls import reverse
from users.tests.conftest import general_user
import pytest


@pytest.mark.django_db
def test_custom_login_view_renders_template(client):

    response = client.get(reverse('login'))

    assert response.status_code == 200
    assert 'form' in response.context
    assert 'login.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_custom_login_view_success(client, general_user):

    response = client.post(reverse('login'), {
        'username': 'user_test',
        'password': 'password123'
    })
    user = response.wsgi_request.user

    assert response.status_code == 302
    assert response.url == reverse('index')
    assert user.is_authenticated is True
    assert user.user_status is True


@pytest.mark.django_db
def test_custom_login_view_error(client):

    response = client.post(reverse('login'), {
        'username': 'invalid',
        'password': 'invalid'
    })

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
