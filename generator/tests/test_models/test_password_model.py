from generator.models import Password
from users.tests.conftest import general_user
from generator.utils import Generator
from django.utils import timezone
from freezegun import freeze_time
import pytest


@pytest.mark.django_db
def test_validate_password_creation(general_user):

    with freeze_time("2025-01-01 00:00:00"):

        now = timezone.now()
        password = Generator.generate_password(12)
        entropy = Generator.calculate_entropy(password)
        time_to_decrypt = Generator.calculate_decryption_time(entropy)
        general_password_test = Password.objects.create(
            user=general_user,
            password=password,
            entropy=entropy,
            decryption_years_needed=time_to_decrypt
        )

    assert general_password_test.pk is not None
    assert general_password_test.user == general_user
    assert general_password_test.password == password
    assert general_password_test.entropy == entropy
    assert general_password_test.decryption_years_needed == time_to_decrypt
    assert general_password_test.creation_date == now


@pytest.mark.django_db
def test_validate_duplicated_password(general_user):

    password = Generator.generate_password(12)
    entropy = Generator.calculate_entropy(password)
    time_to_decrypt = Generator.calculate_decryption_time(entropy)
    general_password_test = Password.objects.create(
        user=general_user,
        password=password,
        entropy=entropy,
        decryption_years_needed=time_to_decrypt
    )

    new_general_password_test = Password.objects.create(
        user=general_user,
        password=password,
        entropy=entropy,
        decryption_years_needed=time_to_decrypt
    )

    assert general_password_test != new_general_password_test
    assert general_password_test.pk != new_general_password_test.pk
