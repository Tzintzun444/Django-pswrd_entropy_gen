from generator.permissions import PasswordPermission
from rest_framework.test import APIRequestFactory
from unittest.mock import Mock
import pytest

factory = APIRequestFactory()


@pytest.mark.parametrize('action,is_authenticated,expected', [
    ('create', True, True),
    ('create', False, False),
    ('list', True, True),
    ('list', False, False),
    ('other', False, True)
])
def test_custom_user_permission_has_permission(action, is_authenticated, expected):

    request_user = Mock()
    request_user.is_authenticated = is_authenticated

    request = factory.get('/fake-url/')
    request.user = request_user

    mock_view = type("View", (), {'action': action})()

    permission = PasswordPermission()

    assert permission.has_permission(request, mock_view) is expected


@pytest.mark.parametrize('action,is_owner,is_staff,is_superuser,expected', [
    ('retrieve', True, False, False, True),
    ('retrieve', False, False, True, True),
    ('retrieve', False, True, False, True),
    ('retrieve', False, False, False, False),
    ('retrieve', True, True, True, True),
    ('destroy', True, False, False, True),
    ('destroy', False, False, True, True),
    ('destroy', False, True, False, True),
    ('destroy', False, False, False, False),
    ('destroy', True, True, True, True),
    ('other', True, True, True, False)
])
@pytest.mark.django_db
def test_custom_user_permission_has_object_permission(general_user, action, is_owner, is_staff, is_superuser, expected):

    request_user = general_user
    request_user.is_staff = is_staff
    request_user.is_superuser = is_superuser

    request = factory.get('/fake-url/')
    request.user = request_user

    obj = type('Obj', (), {'owner': general_user if is_owner else type('CustomUser', (), {'username': 'another_user'})})
    mock_view = type('View', (), {'action': action})

    permission = PasswordPermission()

    assert permission.has_object_permission(request, mock_view, obj) is expected
