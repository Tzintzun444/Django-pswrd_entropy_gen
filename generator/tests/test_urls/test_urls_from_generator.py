from generator.views import CreatePasswordView, PasswordListView, PasswordDeleteView, SavePasswordView
from generator.viewsets import PasswordViewSet, AllPasswordsViewSet
from django.urls import reverse, resolve
import pytest


@pytest.mark.parametrize('url,args,url_name,view,from_DRF', [
    ('generate-passwords/', None, 'generator', CreatePasswordView, False),
    ('my-passwords/', None, 'my_passwords', PasswordListView, False),
    ('delete-password/1/', [1], 'delete_password', PasswordDeleteView, False),
    ('save-password/', None, 'save_password', SavePasswordView, False),
    ('api/passwords/', None, 'password-list', PasswordViewSet, True),
    ('api/passwords/1/', [1], 'password-detail', PasswordViewSet, True),
    ('api/all-passwords/', None, 'all_passwords-list', AllPasswordsViewSet, True),
    ('api/all-passwords/1/', [1], 'all_passwords-detail', AllPasswordsViewSet, True)
])
def test_users_urls_with_reverse_and_resolve(url, args, url_name, view, from_DRF):

    url = '/generator/' + url
    url_from_reverse = reverse(url_name, args=args)

    assert url_from_reverse == url

    match = resolve(url)

    assert match.view_name == url_name

    if from_DRF:

        assert match.func.cls == view

    else:

        assert match.func.view_class == view
