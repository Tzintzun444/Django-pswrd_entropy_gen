import pytest

from users.forms import VerificationEmailForm, CodeInputWidget

data = {}
for index in range(6):
    data[f'code_{index}'] = f'{index + 1}'


def test_widget_decompress_method():

    widget = CodeInputWidget()

    assert widget.decompress('123456') == ['1', '2', '3', '4', '5', '6']
    assert widget.decompress('') == ['', '', '', '', '', '']


def test_widget_value_from_datadict_method():

    widget = CodeInputWidget()
    value = widget.value_from_datadict(data=data, files={}, name='code')

    assert value == '123456'


def test_verification_email_form_with_valid_data():

    form = VerificationEmailForm(data=data)

    assert form.is_valid()
    assert 'code' in form.fields


def test_verification_email_form_length_error():

    data = {
        'code_0': '0'
    }

    form = VerificationEmailForm(data=data)

    assert form.is_valid() is False
    assert 'code' in form.errors
    assert 'Code must be 6 digits' in form.errors['code']


def test_verification_email_form_raises_type_error_when_not_input_numbers():

    data['code_0'] = 1
    form = VerificationEmailForm(data=data)

    with pytest.raises(TypeError):
        form.is_valid()
