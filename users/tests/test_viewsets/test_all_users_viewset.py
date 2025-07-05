from users.viewsets import AllUsersViewSet
from users.serializers import CustomAdminSerializer
from users.permissions import IsStaffOrAdmin
from users.models import CustomUser
from users.tests.conftest import api_client_auth_with_admin, admin_user, general_user
from django.urls import reverse
import pytest


def test_all_users_viewset_attributes():

    viewset = AllUsersViewSet()

    assert viewset.serializer_class == CustomAdminSerializer
    assert viewset.permission_classes == [IsStaffOrAdmin]


@pytest.mark.django_db
def test_all_users_viewset_list_action(api_client_auth_with_admin, general_user):

    response = api_client_auth_with_admin.get(reverse('all-users-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == len(CustomUser.objects.all())


@pytest.mark.django_db
def test_all_users_viewset_list_action_with_not_admin_user(api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.get((reverse('all-users-list')))

    assert response.status_code == 403


@pytest.mark.django_db
def test_all_users_viewset_retrieve_action(api_client_auth_with_admin, admin_user):

    response = api_client_auth_with_admin.get(reverse('all-users-detail', args=[admin_user.pk]))

    assert response.status_code == 200
    assert response.data['id'] == admin_user.pk
    assert response.data['username'] == admin_user.username
    assert response.data['email'] == admin_user.email


@pytest.mark.django_db
def test_all_users_viewset_retrieve_action_with_non_existent_pk(api_client_auth_with_admin):

    response = api_client_auth_with_admin.get(reverse('all-users-detail', args=[10000012]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_all_users_viewset_not_allowed_methods(api_client_auth_with_admin):

    data = {'username': 'fake_username'}
    response = api_client_auth_with_admin.post(reverse('all-users-list'), data=data)

    assert response.status_code == 405
