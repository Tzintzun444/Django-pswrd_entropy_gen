from users.tests.conftest import auth_user, general_user
from generator.models import Password
from django.urls import reverse
import pytest


def test_save_password_view_redirects_not_auth_users(client):

    response = client.get(reverse('save_password'))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('save_password')


@pytest.mark.django_db
def test_save_password_view_returns_405_in_get(auth_user):

    response = auth_user.get(reverse('save_password'))

    assert response.status_code == 405


@pytest.mark.django_db
def test_save_password_view_saves_password(auth_user, general_user):

    password = 'password/123'
    data = {
        'password': password
    }

    response = auth_user.post(reverse('save_password'), data=data)

    assert response.status_code == 302
    assert response.url == reverse('my_passwords')

    general_user.refresh_from_db()

    assert password == Password.objects.filter(user=general_user, password=password).first().password
    assert Password.objects.filter(user=general_user, password=password).exists() is True
