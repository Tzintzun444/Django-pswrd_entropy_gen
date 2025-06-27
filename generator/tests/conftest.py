from generator.models import Password
from generator.utils import Generator
from users.tests.conftest import general_user
import pytest


@pytest.fixture
@pytest.mark.django_db
def general_password(general_user):

    password = Generator.generate_password(12)
    entropy = Generator.calculate_entropy(password)
    time_to_decrypt = Generator.calculate_decryption_time(entropy)
    general_password = Password.objects.create(
        user=general_user,
        password=password,
        entropy=entropy,
        decryption_years_needed=time_to_decrypt
    )

    return general_password
