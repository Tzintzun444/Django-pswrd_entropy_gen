from users.views import (UserSettingsView, SignUpUserView, VerifyEmailUserView, CustomLogInView, CustomLogOutView,
                         DeleteUserView, unlink_oauth_google, ResendCodeView)
from users.viewsets import CustomClientViewSet, CustomAdminViewSet, AllUsersViewSet
from django.urls import resolve, reverse
from django.views.i18n import set_language
import pytest


@pytest.mark.parametrize('url,args,url_name,view,is_CBV,from_DRF', [
    ('settings/', None, 'settings', UserSettingsView, True, False),
    ('sign-up/', None, 'sign_up', SignUpUserView, True, False),
    ('verify-email/', None, 'verify_email', VerifyEmailUserView, True, False),
    ('resend-code/', None, 'resend_code', ResendCodeView, True, False),
    ('login/', None, 'login', CustomLogInView, True, False),
    ('logout/', None, 'logout', CustomLogOutView, True, False),
    ('delete-user/', None, 'delete_user', DeleteUserView, True, False),
    ('set-language/', None, 'set_language', set_language, False, False),
    ('api/customers/', None, 'customer-list', CustomClientViewSet, True, True),
    ('api/customers/1/', [1], 'customer-detail', CustomClientViewSet, True, True),
    ('api/admins/', None, 'admin-list', CustomAdminViewSet, True, True),
    ('api/admins/1/', [1], 'admin-detail', CustomAdminViewSet, True, True),
    ('api/all-users/', None, 'all-users-list', AllUsersViewSet, True, True),
    ('api/all-users/1/', [1], 'all-users-detail', AllUsersViewSet, True, True)
])
def test_users_urls_with_reverse_and_resolve(url, args, url_name, view, is_CBV, from_DRF):

    url = '/users/' + url
    url_from_reverse = reverse(url_name, args=args)

    assert url_from_reverse == url

    match = resolve(url)

    assert match.view_name == url_name

    if is_CBV:

        if from_DRF:

            assert match.func.cls == view

        else:

            assert match.func.view_class == view

    else:

        assert match.func == view


def test_unlink_google_with_reverse_and_resolve():

    url = '/users/unlink-google/'

    assert url == reverse('unlink_google')

    match = resolve('/users/unlink-google/')

    assert match.view_name == 'unlink_google'
    assert match.func.__name__ == unlink_oauth_google.__name__
