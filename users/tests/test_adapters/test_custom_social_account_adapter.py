from users.adapters import CustomSocialAccountAdapter
from users.tests.conftest import admin_user
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from allauth.socialaccount.models import SocialLogin
from unittest.mock import Mock
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_custom_social_account_adapter_pre_social_login_method_connects_existing_user(admin_user):

    adapter = CustomSocialAccountAdapter()

    social_user = User(email=admin_user.email)
    sociallogin = Mock(spec=SocialLogin)
    sociallogin.user = social_user
    sociallogin.account = Mock()
    sociallogin.connect = Mock()

    factory = RequestFactory()
    request = factory.get('/')
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

    response = adapter.pre_social_login(request, sociallogin)

    sociallogin.connect.assert_called_once_with(request, admin_user)

    assert response.status_code == 302


def test_custom_social_account_adapter_pre_social_login_method_does_nothing_when_sociallogin_user_has_id():

    adapter = CustomSocialAccountAdapter()

    user = Mock()
    user.id = 123
    sociallogin = Mock()
    sociallogin.user = user

    response = adapter.pre_social_login(Mock(), sociallogin)

    assert response is None


@pytest.mark.django_db
def test_custom_social_account_populate_user_method_gives_username():

    adapter = CustomSocialAccountAdapter()

    sociallogin = Mock()
    sociallogin.account.extra_data = {
        'given_name': 'Juan',
        'family_name': 'Pérez'
    }

    data = {'email': 'juan.perez+test@gmail.com'}
    request = Mock()

    user = adapter.populate_user(request, sociallogin, data)

    assert user.username == 'juan.pereztest'
    assert user.first_name == 'Juan'
    assert user.last_name == 'Pérez'


@pytest.mark.django_db
def test_custom_social_account_populate_user_method_gives_username_from_email(admin_user):

    adapter = CustomSocialAccountAdapter()

    sociallogin = Mock()
    sociallogin.account.extra_data = {}

    data = {'email': f'{admin_user.username}@mail.com'}
    request = Mock()

    user = adapter.populate_user(request, sociallogin, data)

    assert user.username == f'{admin_user.username}@mail.com'
