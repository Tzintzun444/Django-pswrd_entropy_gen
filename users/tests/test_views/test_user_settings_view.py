from django.urls import reverse
from users.tests.conftest import general_user
import pytest


@pytest.mark.django_db
def test_user_settings_view_renders_with_context(auth_user):

    response = auth_user.get(reverse('settings'))

    assert response.status_code == 200
    assert 'settings.html' in [t.name for t in response.templates]
    assert 'has_password' in response.context
    assert response.context['has_password'] is True
    assert 'linked_google_account' in response.context
    assert response.context['linked_google_account'] is False


@pytest.mark.django_db
def test_user_settings_view_changes_data(auth_user, general_user):

    data = {
        'username': 'new_username',
        'first_name': 'new_first_name',
        'last_name': general_user.last_name,
        'email': general_user.email,


    }
    response = auth_user.post(reverse('settings'), data=data)

    assert response.status_code == 302
    assert response.url == reverse('settings')

    general_user.refresh_from_db()

    assert general_user.username == 'new_username'
    assert general_user.first_name == 'new_first_name'
    assert general_user.last_name == 'last_name'
    assert general_user.email == 'email@example.com'
    assert general_user.check_password('password123') is True


def test_user_settings_view_with_not_auth_user(client):

    response = client.get(reverse('settings'))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('settings')
