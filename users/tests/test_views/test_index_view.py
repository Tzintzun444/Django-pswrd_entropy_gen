from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_IndexView(client):
    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert 'index.html' in [t.name for t in response.templates]
