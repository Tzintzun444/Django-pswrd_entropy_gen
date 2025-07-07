from django.urls import reverse
from django.contrib.auth import get_user_model
from users.tests.conftest import general_user
import pytest


User = get_user_model()


@pytest.mark.django_db
def test_delete_user_raises_405_in_get(auth_user, general_user):

    response = auth_user.get(reverse('delete_user'))

    assert response.status_code == 405

    general_user.refresh_from_db()

    assert User.objects.filter(username=general_user.username).exists() is True
    

def test_delete_user_with_not_auth_user(client):

    response = client.post(reverse('delete_user'))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('delete_user')


@pytest.mark.django_db
def test_delete_user_works(auth_user):

    response = auth_user.post(reverse('delete_user'))

    assert response.status_code == 302
    assert response.url == reverse('index')
    assert User.objects.filter(username='user_test').exists() is False
