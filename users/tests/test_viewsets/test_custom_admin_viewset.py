from users.viewsets import CustomAdminViewSet
from users.serializers import CustomAdminSerializer
from users.permissions import IsStaffOrAdmin
from users.models import CustomUser
from users.tests.conftest import general_user, admin_user, api_client_auth_with_admin, api_client_auth_with_general_user
from rest_framework.test import APIRequestFactory, APIClient
from django.urls import reverse
import pytest

factory = APIRequestFactory()


@pytest.mark.django_db
def test_custom_admin_viewset_attributes(general_user):

    viewset = CustomAdminViewSet()

    assert viewset.serializer_class == CustomAdminSerializer
    assert viewset.permission_classes == [IsStaffOrAdmin]
    assert list(viewset.queryset) == list(CustomUser.objects.filter(is_staff=True))


@pytest.mark.django_db
def test_custom_admin_viewset_list_action_with_not_auth_user(general_user):

    client = APIClient()
    response = client.get(reverse('admin-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_custom_admin_viewset_list_action_with_general_user(general_user, api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.get(reverse('admin-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_custom_admin_viewset_list_action_with_admin_user(admin_user, api_client_auth_with_admin):

    CustomUser.objects.create(
        username='anewusername',
        first_name='name',
        last_name='name',
        email='newemail1@example.com',
        is_verified=True,
        is_staff=True,
        is_superuser=True,
        password='1233545dfgdgsdgf'
    )

    response = api_client_auth_with_admin.get(reverse('admin-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_custom_admin_viewset_retrieve_action_with_not_owner_user(general_user, api_client_auth_with_admin):

    user = CustomUser.objects.create(
        username='anewusername',
        first_name='name',
        last_name='name',
        email='newemail1@example.com',
        is_verified=True,
        is_staff=True,
        is_superuser=True,
        password='1233545dfgdgsdgf'
    )
    response = api_client_auth_with_admin.get(reverse('admin-detail', args=[user.pk]))

    assert response.status_code == 200
    assert response.data['username'] == user.username


@pytest.mark.django_db
def test_custom_admin_viewset_retrieve_action_with_owner_user(admin_user, api_client_auth_with_admin):

    response = api_client_auth_with_admin.get(reverse('admin-detail', args=[admin_user.pk]))

    assert response.status_code == 200
    assert response.data['id'] == admin_user.id
    assert response.data['username'] == admin_user.username
    assert response.data['email'] == admin_user.email


@pytest.mark.django_db
def test_custom_admin_viewset_retrieve_action_with_general_user_returns_403(
        admin_user, api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.get(reverse('admin-detail', args=[admin_user.pk]))

    assert response.status_code == 403


@pytest.mark.parametrize('is_admin,is_auth,status_code', [
    (True, False, 201),
    (False, True, 403),
    (False, False, 403)
])
@pytest.mark.django_db
def test_custom_admin_viewset_create_action(general_user, admin_user, is_admin, is_auth, status_code):

    data = {
        'username': 'anewusername',
        'first_name': 'name',
        'last_name': 'name',
        'email': 'newemail1@example.com',
        'password': '1233545dfgdgsdgf'
    }
    client = APIClient()

    if is_admin:
        client.force_authenticate(user=admin_user)
    elif is_auth:
        client.force_authenticate(user=general_user)

    response = client.post(reverse('admin-list'), data=data)
    user = CustomUser.objects.filter(username='anewusername', email='newemail1@example.com')

    assert response.status_code == status_code

    if is_admin:
        assert user.exists() is True
        assert user.first().check_password('1233545dfgdgsdgf') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 200),
    (False, True, 403),
    (False, False, 403)
])
@pytest.mark.django_db
def test_custom_admin_viewset_partial_update_action_with_auth_users(
        general_user, admin_user, is_admin, is_owner, status_code):

    client = APIClient()
    data = {
        'username': 'anewusername',
        'password': 'new_password'
    }

    if is_admin:

        client.force_authenticate(user=admin_user)

    elif is_owner:
        client.force_authenticate(user=general_user)

    else:

        user = CustomUser.objects.create(
            username='anewusername',
            first_name='name',
            last_name='name',
            email='newemail1@example.com',
            is_verified=True,
            is_staff=False,
            is_superuser=False,
            password='1233545dfgdgsdgf'
        )
        client.force_authenticate(user=user)

    response = client.patch(reverse('admin-detail', args=[admin_user.pk]), data=data)
    admin_user.refresh_from_db()

    assert response.status_code == status_code

    if is_admin:
        assert response.data['username'] == 'anewusername' == admin_user.username
        assert response.data['password'] == admin_user.password != 'new_password'
        assert admin_user.check_password('new_password') is True


@pytest.mark.django_db
def test_custom_admin_viewset_partial_update_action_with_not_auth_user(admin_user):
    data = {
        'username': 'anewusername',
        'password': 'new_password'
    }
    client = APIClient()
    response = client.patch(reverse('admin-detail', args=[admin_user.pk]), data=data)
    admin_user.refresh_from_db()

    assert response.status_code == 403
    assert admin_user.username == 'user_admin_test'
    assert admin_user.check_password('password123') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 200),
    (False, True, 403),
    (False, False, 403)
])
@pytest.mark.django_db
def test_custom_admin_viewset_update_action_with_auth_users(general_user, admin_user, is_admin, is_owner, status_code):

    client = APIClient()
    data = {
        'username': 'anewusername',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
        'email': 'new_email123@mail.com',
        'password': 'new_password'
    }

    if is_admin:

        client.force_authenticate(user=admin_user)

    elif is_owner:
        client.force_authenticate(user=general_user)

    else:

        user = CustomUser.objects.create(
            username='anewusername',
            first_name='name',
            last_name='name',
            email='newemail1@example.com',
            is_verified=True,
            is_staff=False,
            is_superuser=False,
            password='1233545dfgdgsdgf'
        )
        client.force_authenticate(user=user)

    response = client.put(reverse('admin-detail', args=[admin_user.pk]), data=data)
    admin_user.refresh_from_db()

    assert response.status_code == status_code

    if is_admin:
        assert response.data['username'] == 'anewusername' == admin_user.username
        assert response.data['password'] == admin_user.password != 'new_password'
        assert admin_user.check_password('new_password') is True


@pytest.mark.django_db
def test_custom_admin_viewset_update_action_with_not_auth_user(admin_user):

    data = {
        'username': 'anewusername',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
        'email': 'new_email123@mail.com',
        'password': 'new_password'
    }
    client = APIClient()
    response = client.put(reverse('admin-detail', args=[admin_user.pk]), data=data)
    admin_user.refresh_from_db()

    assert response.status_code == 403
    assert admin_user.username == 'user_admin_test'
    assert admin_user.check_password('password123') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 204),
    (False, True, 403),
    (False, False, 403)
])
@pytest.mark.django_db
def test_custom_admin_viewset_destroy_action_with_auth_users(
        general_user, admin_user, is_admin, is_owner, status_code):

    client = APIClient()

    if is_admin:

        client.force_authenticate(user=admin_user)

    elif is_owner:

        client.force_authenticate(user=general_user)

    else:

        user = CustomUser.objects.create(
            username='anewusername',
            first_name='name',
            last_name='name',
            email='newemail1@example.com',
            is_verified=True,
            is_staff=False,
            is_superuser=False,
            password='1233545dfgdgsdgf'
        )
        client.force_authenticate(user=user)

    response = client.delete(reverse('admin-detail', args=[admin_user.pk]))

    assert response.status_code == status_code

    if is_admin:

        assert CustomUser.objects.filter(pk=admin_user.pk).exists() is False


@pytest.mark.django_db
def test_custom_admin_viewset_destroy_action_with_not_auth_users(admin_user):

    client = APIClient()
    response = client.delete(reverse('admin-detail', args=[admin_user.pk]))

    assert response.status_code == 403
    assert CustomUser.objects.filter(pk=admin_user.pk).exists() is True
