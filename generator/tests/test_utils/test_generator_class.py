from generator.utils import Generator
from typing import Union
import string
import pytest


@pytest.mark.parametrize('length,uppercase,numbers,punctuations,customized,not_allowed', [
    (12, True, True, True, '', ''),
    (16, True, True, True, '1234567890ñ', ''),
    (12, False, False, False, '456A<*/x', 'pqrst'),
    (12, True, True, False, '', ''),
    (12, True, False, False, '', ''),
    (12, False, False, False, '', ''),
    (12, True, False, True, '', ''),
    (12, False, False, True, '', ''),
    (12, True, True, True, 'tzx4', '986y'),
    (12, False, True, False, 'A', '123456789'),
    (20, True, True, True, 'ñ!#$%&/', 'amnoXGFASDF1234234?'),
    (30, True, True, True, '', ''),
    (12, True, True, True, None, None),
    (10, True, True, True, '123456', '')
])
def test_generator_class_generate_password_method_works(
        length, uppercase, numbers, punctuations, customized, not_allowed
):

    situations = (
        (uppercase, string.ascii_uppercase),
        (numbers, string.digits),
        (punctuations, '!#$%&*+_-/')
    )
    remaining_characters = length - len(customized) if customized else length

    for situation in situations:

        if situation[0]:

            remaining_characters -= 1

    assert remaining_characters >= 0

    password = Generator.generate_password(
        length=length,
        use_uppercase=uppercase,
        use_numbers=numbers,
        use_punctuations=punctuations,
        customized=customized,
        not_allowed=not_allowed
    )

    assert len(password) == length

    for situation in situations:

        if situation[0]:

            assert any(letter in password for letter in situation[1]) is True

    if customized:

        assert all(letter in password for letter in customized) is True

    if not_allowed:

        assert all([letter not in password for letter in not_allowed]) is True


@pytest.mark.parametrize('length,uppercase,numbers,punctuations,customized,not_allowed,error', [
    ('0', True, True, True, '', '', TypeError),
    (0, True, True, True, '', '', ValueError),
    (-1, True, True, True, '', '', ValueError),
    (12, 'True', 'True', 17, '', '', TypeError),
    (12, 17, 18, True, '', '', TypeError),
    (12, True, 'False', False, '', '', TypeError),
    (12, 'false', 'false', 'false', '', '', TypeError),
    (12, True, True, True, True, '', TypeError),
    (12, True, True, True, '', True, TypeError),
    (12, True, True, True, '123', '123', ValueError),
    (12, True, True, True, 'lmnox', '123456x', ValueError),
    (12, True, True, True, '', '0a1b2c3d4e5f6g7h8i9j', ValueError),
    (12, True, True, True, '', string.ascii_lowercase, ValueError),
    (12, True, True, True, '', string.ascii_uppercase, ValueError),
    (12, True, True, True, '', string.digits, ValueError),
    (12, True, True, True, '', '!#$%&*+_-/', ValueError),
    (10, True, True, True, '0123456789', '', ValueError),
    (10, True, True, True, '1234567', '', ValueError)
])
def test_generator_class_generate_password_method_raises_errors(
        length, uppercase, numbers, punctuations, customized, not_allowed, error
):

    with pytest.raises(error):

        Generator.generate_password(
            length=length,
            use_uppercase=uppercase,
            use_numbers=numbers,
            use_punctuations=punctuations,
            customized=customized,
            not_allowed=not_allowed
        )


@pytest.mark.parametrize('password,decimals', [
    ('password123N!', 3),
    ('pQ$4alsñkdfjlaskdfa', 6),
    ('pass', 0),
    ('jksladfhkashfjklh44$R', 0),
    ('', 0)
])
def test_generator_class_calculate_entropy_method_works(password, decimals):

    entropy = Generator.calculate_entropy(password, decimals=decimals)

    assert isinstance(entropy, Union[int, float]) is True
    assert entropy > 0 if len(password) > 0 else entropy == 0

    if isinstance(entropy, float):
        # assert str(entropy) == 1
        decimals_from_entropy = str(entropy).split('.')[1]

        assert len(decimals_from_entropy) <= decimals


@pytest.mark.parametrize('password,decimals,error', [
    (17, 'password', TypeError),
    ('password123', 17.5, TypeError),
    ('password123', -2, ValueError)
])
def test_generator_class_calculate_entropy_method_raises_errors(password, decimals, error):

    with pytest.raises(error):

        Generator.calculate_entropy(password, decimals=decimals)


@pytest.mark.parametrize('entropy,decimals,attempts_per_second', [
    (120, 2, 1e12),
    (100, 5, 2),
    (75, 6, 1e14)
])
def test_generator_class_calculate_decryption_time_method_works(entropy, decimals, attempts_per_second):

    decryption_time = Generator.calculate_decryption_time(
        entropy, decimals=decimals, attempts_per_second=attempts_per_second
    )

    assert decryption_time > 0
    assert isinstance(decryption_time, Union[int, float]) is True

    if isinstance(decryption_time, float) and 'e' in str(decryption_time):

        number_without_exp = str(decryption_time).split('e')[0]
        decimals_from_time = number_without_exp.split('.')[1]

        assert len(decimals_from_time) <= decimals

    elif isinstance(decryption_time, float):

        decimals_from_time = str(decryption_time).split('.')[1]
        assert len(decimals_from_time) <= decimals


@pytest.mark.parametrize('entropy,decimals,attempts_per_second,error', [
    ('12', 2, 1e12, TypeError),
    (12, 1.5, 1e12, TypeError),
    (12, -2, 1e12, ValueError),
    (12, 2, '1e12', TypeError),
    (12, 2, 0, ValueError),
    (12, 2, -1, ValueError)
])
def test_generator_class_calculate_decryption_time_method_raises_errors(entropy, decimals, attempts_per_second, error):

    with pytest.raises(error):

        Generator.calculate_decryption_time(entropy, decimals=decimals, attempts_per_second=attempts_per_second)


@pytest.mark.parametrize('length,valid', [
    (12, True),
    (20, True),
    (10, True),
    (1, False),
    (-2, False),
    ('1', False),
    (True, False)
])
def test_generator_class_create_password_method(length, valid):

    password, entropy, decryption_time = Generator(length).create_password()

    if valid:

        assert isinstance(password, str) is True
        assert len(password) == length
        assert entropy == Generator.calculate_entropy(password)
        assert decryption_time == Generator.calculate_decryption_time(entropy)

    else:

        assert password is None and entropy is None and decryption_time is None


@pytest.mark.parametrize('length,valid', [
    (12, True),
    (20, True),
    (10, True),
    (1, False),
    (-2, False),
    ('1', False),
    (True, False)
])
def test_generator_class_(length, valid):

    generator = Generator(length)
    password = generator.password
    entropy = generator.entropy
    decryption_time = generator.decryption_time

    if valid:

        assert isinstance(password, str) is True
        assert len(password) == length
        assert entropy == Generator.calculate_entropy(password)
        assert decryption_time == Generator.calculate_decryption_time(entropy)

    else:

        assert password is None and entropy is None and decryption_time is None
