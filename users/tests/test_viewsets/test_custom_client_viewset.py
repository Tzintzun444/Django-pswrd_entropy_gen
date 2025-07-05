from users.viewsets import CustomClientViewSet
from users.serializers import CustomCustomerSerializer
from users.permissions import CustomUserPermission
from users.models import CustomUser
from users.tests.conftest import general_user, admin_user, api_client_auth_with_admin, api_client_auth_with_general_user
from rest_framework.test import APIRequestFactory, APIClient
from django.urls import reverse
import pytest

factory = APIRequestFactory()


@pytest.mark.django_db
def test_custom_client_viewset_attributes(general_user):

    viewset = CustomClientViewSet()

    assert viewset.serializer_class == CustomCustomerSerializer
    assert viewset.permission_classes == [CustomUserPermission]
    assert list(viewset.queryset) == list(CustomUser.objects.filter(is_staff=False))


@pytest.mark.django_db
def test_custom_client_viewset_list_action_with_not_auth_user(general_user):

    client = APIClient()
    response = client.get(reverse('customer-list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_custom_client_viewset_list_action_with_general_user(general_user, api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.get(reverse('customer-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 1


@pytest.mark.django_db
def test_custom_client_viewset_list_action_with_admin_user(admin_user, general_user, api_client_auth_with_admin):

    CustomUser.objects.create(
        username='anewusername',
        first_name='name',
        last_name='name',
        email='newemail1@example.com',
        is_verified=True,
        is_staff=False,
        is_superuser=False,
        password='1233545dfgdgsdgf'
    )

    response = api_client_auth_with_admin.get(reverse('customer-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_custom_client_viewset_retrieve_action_with_not_owner_user(general_user, api_client_auth_with_general_user):

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
    response = api_client_auth_with_general_user.get(reverse('customer-detail', args=[user.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_custom_client_viewset_retrieve_action_with_owner_user(general_user, api_client_auth_with_general_user):

    response = api_client_auth_with_general_user.get(reverse('customer-detail', args=[general_user.pk]))

    assert response.status_code == 200
    assert response.data['id'] == general_user.id
    assert response.data['username'] == general_user.username
    assert response.data['email'] == general_user.email


@pytest.mark.django_db
def test_custom_client_viewset_retrieve_action_with_admin_user(
        general_user, api_client_auth_with_admin):

    response = api_client_auth_with_admin.get(reverse('customer-detail', args=[general_user.pk]))

    assert response.status_code == 200
    assert response.data['id'] == general_user.id
    assert response.data['username'] == general_user.username
    assert response.data['email'] == general_user.email


@pytest.mark.parametrize('is_admin,is_auth', [
    (True, False),
    (False, True),
    (False, False)
])
@pytest.mark.django_db
def test_custom_client_viewset_create_action(general_user, admin_user, is_admin, is_auth):

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

    response = client.post(reverse('customer-list'), data=data)
    user = CustomUser.objects.filter(username='anewusername', email='newemail1@example.com')
    assert response.status_code == 201
    assert user.exists() is True
    assert user.first().check_password('1233545dfgdgsdgf') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 200),
    (False, True, 200),
    (False, False, 404)
])
@pytest.mark.django_db
def test_custom_client_viewset_partial_update_action_with_auth_users(
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

    response = client.patch(reverse('customer-detail', args=[general_user.pk]), data=data)
    general_user.refresh_from_db()

    assert response.status_code == status_code

    if is_admin or is_owner:
        assert response.data['username'] == 'anewusername' == general_user.username
        assert response.data['password'] == general_user.password != 'new_password'
        assert general_user.check_password('new_password') is True


@pytest.mark.django_db
def test_custom_client_viewset_partial_update_action_with_not_auth_user(general_user):
    data = {
        'username': 'anewusername',
        'password': 'new_password'
    }
    client = APIClient()
    response = client.patch(reverse('customer-detail', args=[general_user.pk]), data=data)
    general_user.refresh_from_db()

    assert response.status_code == 404
    assert general_user.username == 'user_test'
    assert general_user.check_password('password123') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 200),
    (False, True, 200),
    (False, False, 404)
])
@pytest.mark.django_db
def test_custom_client_viewset_update_action_with_auth_users(general_user, admin_user, is_admin, is_owner, status_code):

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

    response = client.put(reverse('customer-detail', args=[general_user.pk]), data=data)
    general_user.refresh_from_db()

    assert response.status_code == status_code

    if is_admin or is_owner:
        assert response.data['username'] == 'anewusername' == general_user.username
        assert response.data['password'] == general_user.password != 'new_password'
        assert general_user.check_password('new_password') is True


@pytest.mark.django_db
def test_custom_client_viewset_update_action_with_not_auth_user(general_user):

    data = {
        'username': 'anewusername',
        'first_name': 'new_first_name',
        'last_name': 'new_last_name',
        'email': 'new_email123@mail.com',
        'password': 'new_password'
    }
    client = APIClient()
    response = client.put(reverse('customer-detail', args=[general_user.pk]), data=data)
    general_user.refresh_from_db()

    assert response.status_code == 404
    assert general_user.username == 'user_test'
    assert general_user.check_password('password123') is True


@pytest.mark.parametrize('is_admin,is_owner,status_code', [
    (True, False, 204),
    (False, True, 204),
    (False, False, 404)
])
@pytest.mark.django_db
def test_custom_client_viewset_destroy_action_with_auth_users(
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

    response = client.delete(reverse('customer-detail', args=[general_user.pk]))

    assert response.status_code == status_code

    if is_admin or is_owner:

        assert CustomUser.objects.filter(pk=general_user.pk).exists() is False


@pytest.mark.django_db
def test_custom_client_viewset_destroy_action_with_not_auth_users(general_user):

    client = APIClient()
    response = client.delete(reverse('customer-detail', args=[general_user.pk]))

    assert response.status_code == 404
    assert CustomUser.objects.filter(pk=general_user.pk).exists() is True
