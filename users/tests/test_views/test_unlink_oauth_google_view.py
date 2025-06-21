from django.urls import reverse
from users.tests.conftest import general_user
import pytest


@pytest.mark.django_db
def test_unlink_oauth_google_view_raises_404_in_get(client, general_user):

    client.force_login(general_user)
    response = client.get(reverse('unlink_google'))

    assert response.status_code == 404
