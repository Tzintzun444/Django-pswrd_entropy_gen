from users.permissions import IsStaffOrAdmin
from rest_framework.test import APIRequestFactory
import pytest

factory = APIRequestFactory()


@pytest.mark.parametrize('is_staff,is_superuser,expected', [
    (True, True, True),
    (True, False, True),
    (False, True, True),
    (False, False, False)
])
@pytest.mark.django_db
def test_is_staff_or_admin_has_permission_method(general_user, is_staff, is_superuser, expected):

    general_user.is_staff = is_staff
    general_user.is_superuser = is_superuser
    general_user.save()

    request = factory.get('/fake-url/')
    request.user = general_user

    mock_view = object()

    permission = IsStaffOrAdmin()

    assert permission.has_permission(request, mock_view) is expected


@pytest.mark.parametrize('is_staff,is_superuser,expected', [
    (True, True, True),
    (True, False, True),
    (False, True, True),
    (False, False, False)
])
@pytest.mark.django_db
def test_is_staff_or_admin_has_object_permission_method(general_user, is_staff, is_superuser, expected):

    general_user.is_staff = is_staff
    general_user.is_superuser = is_superuser
    general_user.save()

    request = factory.get('/fake-url/')
    request.user = general_user

    mock_view = object()
    obj = type('Obj', (), {})

    permission = IsStaffOrAdmin()

    assert permission.has_object_permission(request, mock_view, obj) is expected
