from django.urls import reverse
from django.contrib.auth import get_user_model
from users.tests.conftest import auth_user
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_logout_view(client, general_user):

    response_login = client.post(reverse('login'), {
        'username': 'user_test',
        'password': 'password123'
    })

    general_user.refresh_from_db()
    assert response_login.status_code == 302
    assert response_login.url == reverse("index")
    assert general_user.user_status is True

    response_logout = client.post(reverse("logout"))
    general_user.refresh_from_db()

    assert response_logout.status_code == 302
    assert response_logout.url == reverse("index")
    assert general_user.user_status is False
