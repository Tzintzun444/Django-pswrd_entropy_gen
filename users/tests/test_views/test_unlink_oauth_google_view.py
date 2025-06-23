from django.urls import reverse
from users.tests.conftest import general_user
import pytest


@pytest.mark.django_db
def test_unlink_oauth_google_view_raises_404_in_get(auth_user):

    response = auth_user.get(reverse('unlink_google'))

    assert response.status_code == 405
