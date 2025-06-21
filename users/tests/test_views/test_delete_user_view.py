from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404
from users.tests.conftest import general_user
import pytest


User = get_user_model()


@pytest.mark.django_db
def test_delete_user_raises_404_in_get(client, general_user):

    client.force_login(general_user)
    response = client.get(reverse('delete_user'))

    assert response.status_code == 404

    general_user.refresh_from_db()

    assert User.objects.filter(username=general_user.username).exists() is True
    

@pytest.mark.django_db
def test_delete_user_works(client, general_user):

    client.force_login(general_user)
    response = client.post(reverse('delete_user'))

    assert response.status_code == 302
    assert response.url == reverse('index')
    assert User.objects.filter(username='user_test').exists() is False
