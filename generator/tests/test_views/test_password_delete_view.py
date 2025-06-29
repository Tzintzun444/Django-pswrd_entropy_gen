from users.tests.conftest import auth_user, general_user
from generator.models import Password
from django.urls import reverse
import pytest


def test_password_delete_view_redirects_not_auth_users(client):

    response = client.get(reverse('delete_password', args=[1]))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('delete_password', args=[1])


@pytest.mark.django_db
def test_password_delete_view_returns_405_in_get(auth_user, general_user, general_password):

    pk = Password.objects.filter(user=general_user).first().pk
    response = auth_user.get(reverse('delete_password', args=[pk]))

    assert response.status_code == 405


@pytest.mark.django_db
def test_password_delete_view_works(auth_user, general_password):

    pk = general_password.pk
    assert Password.objects.filter(pk=pk).exists() is True

    response = auth_user.post(reverse('delete_password', args=[pk]))

    assert Password.objects.filter(pk=pk).exists() is False
    assert response.status_code == 302
    assert response.url == reverse('my_passwords')


@pytest.mark.django_db
def test_password_delete_view_returns_404_for_non_existent_password(auth_user):

    response = auth_user.post(reverse('delete_password', args=[1000]))

    assert response.status_code == 404
