from users.models import UserNotVerified
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_resend_code_view_returns_405_in_get(client):

    session = client.session
    session['verification_email'] = 'email@example.com'
    session.save()

    response = client.get(reverse('resend_code'))

    assert response.status_code == 405


def test_resend_code_view_redirects_to_sign_up_view(client):

    response = client.post(reverse('resend_code'))

    assert response.status_code == 302
    assert response.url == reverse('sign_up')


@pytest.mark.django_db
def test_resend_code_view_redirects_to_verify_email_view(client):

    session = client.session
    session['verification_email'] = 'correo@example.com'
    session.save()

    UserNotVerified.objects.create(
        email='correo@example.com',
        data={}
    )

    response = client.post(reverse('resend_code'))

    assert response.status_code == 302
    assert response.url == reverse('verify_email')
