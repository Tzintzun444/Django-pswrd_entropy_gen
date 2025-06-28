from generator.models import Password
from generator.utils import Generator
from users.tests.conftest import auth_user
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_password_list_view_redirects_not_auth_users(client):

    response = client.get(reverse('my_passwords'))

    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('my_passwords')


@pytest.mark.django_db
def test_password_list_view_renders_correctly(auth_user):

    response = auth_user.get(reverse('my_passwords'))

    assert response.status_code == 200
    assert 'list-passwords.html' in [t.name for t in response.templates]
    assert 'passwords' in response.context
    assert len(response.context['passwords']) == 0


@pytest.mark.django_db
def test_password_list_view_is_paginated_correctly(auth_user, general_user):

    for _ in range(10):
        password = Generator.generate_password(12)
        entropy = Generator.calculate_entropy(password)
        time_to_decrypt = Generator.calculate_decryption_time(entropy)
        Password.objects.create(
            user=general_user,
            password=password,
            entropy=entropy,
            decryption_years_needed=time_to_decrypt
        )

    response_page_1 = auth_user.get(reverse('my_passwords') + '?page=1')
    page_obj_1 = response_page_1.context['page_obj']
    paginator = response_page_1.context['paginator']

    assert response_page_1.context['is_paginated'] is True
    assert len(response_page_1.context['object_list']) == 5
    assert paginator.num_pages == 2

    assert page_obj_1.number == 1
    assert page_obj_1.has_next() is True
    assert page_obj_1.has_previous() is False

    response_page_2 = auth_user.get(reverse('my_passwords') + '?page=2')
    page_obj_2 = response_page_2.context['page_obj']
    assert page_obj_2.number == 2
    assert page_obj_2.has_next() is False
    assert page_obj_2.has_previous() is True
