from generator.serializers import PasswordModelSerializer
from generator.tests.conftest import general_password, general_user
import pytest


@pytest.mark.django_db
def test_password_model_serializer_with_valid_data(general_user, general_password):

    serializer = PasswordModelSerializer(instance=general_password)
    data = serializer.data

    assert data['id'] == general_password.id
    assert data['user'] == general_user.pk
    assert data['password'] == general_password.password


@pytest.mark.django_db
def test_password_model_serializer_readonly_fields(general_password, general_user):

    serializer = PasswordModelSerializer(data={})
    serializer.is_valid()

    assert 'id' not in serializer.validated_data
    assert 'password' not in serializer.validated_data
    assert 'user' not in serializer.validated_data
    assert 'entropy' not in serializer.validated_data
    assert 'decryption_years_needed' not in serializer.validated_data
