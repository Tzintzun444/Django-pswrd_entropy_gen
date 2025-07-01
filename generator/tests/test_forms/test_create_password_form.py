from generator.forms import CreatePasswordForm

valid_data = {
    'length_password': 12,
    'use_uppercase_letters': True,
    'use_digits': True,
    'use_punctuation_characters': True,
    'custom_characters_allowed': '',
    'characters_not_allowed': ''
}

invalid_data = {
    'length_password': 32,
    'use_uppercase_letters': True,
    'use_digits': True,
    'use_punctuation_characters': True,
    'custom_characters_allowed': 'abcdefghijklmopqrstuvwxyz1234567890/-%!',
    'characters_not_allowed': '123'
}


def test_create_password_form_using_form_valid_data():

    form = CreatePasswordForm(data=valid_data)

    assert form.is_valid() is True
    assert form.cleaned_data['length_password'] == 12
    assert form.cleaned_data['use_uppercase_letters'] is True
    assert form.cleaned_data['use_digits'] is True
    assert form.cleaned_data['use_punctuation_characters'] is True
    assert form.cleaned_data['custom_characters_allowed'] == ''
    assert form.cleaned_data['characters_not_allowed'] == ''


def test_create_password_form_using_form_invalid_data():

    form = CreatePasswordForm(data=invalid_data)

    assert form.is_valid() is False


def test_create_password_form_length_error():

    form = CreatePasswordForm(data=invalid_data)

    assert form.is_valid() is False
    assert 'length_password' in form.errors
    assert 'Must be between 1 to 30' in form.errors['length_password']


def test_create_password_form_crashing_characters_error():

    form = CreatePasswordForm(data=invalid_data)

    assert form.is_valid() is False
    assert 'characters_not_allowed' in form.errors
    assert 'A character is crashing in custom and not allowed characters' in form.errors['characters_not_allowed']


def test_create_password_form_length_custom_characters_greater_than_length_password_error():

    form = CreatePasswordForm(data=invalid_data)

    assert form.is_valid() is False
    assert 'custom_characters_allowed' in form.errors
    assert 'There are more custom characters than available characters in the length of the password.' in form.errors['custom_characters_allowed']