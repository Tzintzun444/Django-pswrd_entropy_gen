from generator.serializers import PasswordGenerationSerializer
from rest_framework.test import APIRequestFactory
import pytest

factory = APIRequestFactory()

data = {
    'length': 12,
    'use_uppercase': True,
    'use_numbers': True,
    'use_punctuations': True,
    'custom_characters': '',
    'characters_not_allowed': ''
}


def test_password_generation_serializer_with_valid_data():

    serializer = PasswordGenerationSerializer(data=data)
    assert serializer.is_valid() is True

    validated_data = serializer.validated_data

    assert 'length' in validated_data
    assert 'use_uppercase' in validated_data
    assert 'use_numbers' in validated_data
    assert 'use_punctuations' in validated_data
    assert 'custom_characters' in validated_data
    assert 'characters_not_allowed' in validated_data

    assert validated_data['length'] == 12
    assert validated_data['use_uppercase'] is True
    assert validated_data['use_numbers'] is True
    assert validated_data['use_punctuations'] is True
    assert validated_data['custom_characters'] == ''
    assert validated_data['characters_not_allowed'] == ''


def test_password_generation_serializer_with_invalid_data():

    data['length'] = True
    data['use_numbers'] = 12

    serializer = PasswordGenerationSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'length' in serializer.errors
    assert 'use_numbers' in serializer.errors


@pytest.mark.django_db
def test_password_generation_serializer_create_method(general_user):

    request = factory.get('/fake-url/')
    request.user = general_user

    serializer = PasswordGenerationSerializer(data=data, context={'request': request})
    assert serializer.is_valid() is True

    instance = serializer.save()
    assert instance.pk is not None
    assert len(instance.password) == 12
    assert instance.user == general_user
