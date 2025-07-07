from django.urls import reverse


def test_IndexView(client):
    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert 'index.html' in [t.name for t in response.templates]
