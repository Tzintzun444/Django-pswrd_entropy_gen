import math
import secrets
import string
from typing import Union


# This is the main class.
class Generator:

    # These are all type of characters available for all the class.
    punctuation_characters = '!#$%&*+_-/'
    type_of_characters = {
        # ABCDEFGHIJKLMNOPQRSTUVWXYZ
        'uppercase': string.ascii_uppercase,
        # 1234567890
        'numbers': string.digits,
        # !#$%&*+_-/
        'punctuations': punctuation_characters
    }

    # The class is initialized with the length of the password as an attribute.
    # The other attributes are given by the create_password method.
    def __init__(self, length):

        # This is the length of the password.
        self._length = length

        # These are the password, its entropy and the time to decrypt it.
        (self._password, self._entropy,
         self._decryption_time) = self.create_password()

    @property
    def length(self):

        return self._length

    @property
    def password(self):

        return self._password

    @property
    def entropy(self):

        return self._entropy

    @property
    def decryption_time(self):

        return self._decryption_time

    # This class method generates a password based on the characters allowed and the provided length.
    @classmethod
    def generate_password(cls, length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True,
                          not_allowed='', customized='') -> str:

        # This is the list that stores the characters of the password.
        password = []
        # abcdefghijklmnopqrstuvwxyz
        characters = string.ascii_lowercase

        # This validates length is an integer.
        if not isinstance(length, int):

            raise TypeError('The number must be a positive integer')

        # This ensures length is a positive integer.
        if length <= 0:

            raise ValueError('The number must be a positive integer')

        # This ensures all arguments for allowing uppercase, numbers and/or punctuations are boolean values.
        if not (
                isinstance(use_uppercase, bool) and isinstance(use_numbers, bool) and isinstance(use_punctuations, bool)
        ):

            raise TypeError('use_uppercase, use_numbers and use_punctuations must be boolean')

        # If custom characters are provided:
        if customized:

            # This ensures the custom characters are a string.
            if not isinstance(customized, str):

                raise TypeError('Customized characters must be a string')

            # This deletes duplicated characters in the custom characters.
            customized = set(customized)

            # This adds the custom characters in the password list.
            password.extend(list(customized))

        # If not allowed characters are provided:
        if not_allowed:

            # This ensures not allowed characters provided are a string.
            if not isinstance(not_allowed, str):

                raise TypeError('Not allowed characters must be a string')

            # This deletes duplicated characters in not allowed characters.
            not_allowed = set(not_allowed)

            # This ensures that there are no identical characters in the custom and not allowed characters.
            if customized and any(letter in customized for letter in not_allowed):

                raise ValueError('A character is crashing in customized and not allowed characters')

            # for each characters string stored as values in the initial dict:
            for characters_string in cls.type_of_characters.values():

                # This ensures not allowed characters doesn't invalid any characters string.
                # If all not allowed characters are the same in a characters string (uppercase, numbers, punctuations)
                # For example, 0123456789 has the same characters of 1234567890, order doesn't matter.
                if all(c in not_allowed for c in characters_string) or all(c in not_allowed for c in string.ascii_lowercase):

                    raise ValueError('Not allowed characters are the same characters of lower, upper, digits or punctuation characters, instead set its parameter as False')

            # For each situation (key) and characters string (value) in the original dict:
            for situation, characters_string in cls.type_of_characters.items():

                # For each character of the not allowed characters:
                for character in not_allowed:

                    # If the character is in a character string:
                    if character in characters_string:

                        # This deletes the character from the characters string and replace the string in the dict.
                        cls.type_of_characters[situation] = cls.type_of_characters[situation].replace(character, '')

                    # If the above condition is not met, and if the character is in the default characters (lowercase)
                    elif character in characters:

                        # This deletes the character from the default characters string and replace it.
                        characters = characters.replace(character, '')

        # This stores the situations in a dictionary as the key, amd their boolean values and the characters related
        # as the values.
        situations = {'uppercase': (use_uppercase, cls.type_of_characters['uppercase']),
                      'numbers': (use_numbers, cls.type_of_characters['numbers']),
                      'punctuations': (use_punctuations, cls.type_of_characters['punctuations']),
                      }

        # This appends a random character from the default (or the characters available if any character was deleted).
        password.append(secrets.choice(characters))

        # The for loop checks if the situations are True or false.
        for character_type in situations.values():

            if character_type[0]:

                # If the situation is allowed (or its parameter is True) adds the specified characters as
                # possibles for the password.
                characters += character_type[1]

                # Also adds 1 character of each type allowed to ensure that there is at least 1.
                password.append(secrets.choice(character_type[1]))

        # This is the necessary length to complete the password.
        remaining = length - len(password)

        # If remaining is negative means that length of the password generated is greater than the provided
        # as an argument.
        if remaining < 0:

            raise ValueError('Length of custom characters is greater than characters available in password, reduce it')

        # If remaining is positive means that lacks characters in the password.
        elif remaining > 0:

            # Selects all necessary characters to complete the password.
            random_password = [secrets.choice(characters) for _ in range(remaining)]

            # Extends the original 'password' list with the list above.
            password.extend(random_password)

        # If remaining equals to 0 means that password has been completed.
        # The 'password' list is shuffled for avoid patterns.
        secrets.SystemRandom().shuffle(password)

        # Finally, the shuffled characters are joined in a string.
        final_password = ''.join(password)

        # Returns the secure password.
        return final_password

    # This class method calculates the entropy of the provided password.
    @classmethod
    def calculate_entropy(cls, password: str, decimals: int = 1) -> Union[int, float]:

        # This ensures the password provided is a string.
        if not isinstance(password, str):

            raise TypeError('password must be a string')

        # This ensures the number of decimals required is an integer.
        if not isinstance(decimals, int):

            raise TypeError('The number of decimals must be an integer')

        # This ensures the number of decimals required is greater than or equal to 0.
        if decimals < 0:

            raise ValueError('The number of decimals must be a positive integer')

        # The set ensures that we don't take repetitive characters.
        unique_characters = set(password)

        # Calculates the length of the password.
        length_password = len(password)

        # Initialize the argument of the log base 2.
        argument_log = 0

        # The dictionary stores the possible characters and the number of them.
        situations = {'uppercase': (cls.type_of_characters['uppercase'], len(cls.type_of_characters['uppercase'])),
                      'lowercase': (string.ascii_lowercase, len(string.ascii_lowercase)),
                      'numbers': (cls.type_of_characters['numbers'], len(cls.type_of_characters['numbers'])),
                      'punctuations': (cls.type_of_characters['punctuations'], len(cls.type_of_characters['punctuations'])),
                      }

        # Separates the characters from the number of possible characters.
        for character_type, possibilities in situations.values():

            # Checks that a character of the specified type appears at least once,
            # this means that the character type is allowed in the password.
            if any(character in character_type for character in unique_characters):

                # If it is true, sums the number of possible characters to the argument of the log.
                argument_log += possibilities

        # Using the previous formula, we calculate its entropy and we verify the formula is not empty.
        entropy = length_password * math.log2(argument_log) if length_password > 0 else 0

        # If entropy is already an integer:
        if isinstance(entropy, int):

            return entropy

        # If the entropy must not have decimals, round to an integer:
        if decimals == 0:

            return round(entropy)

        # Finally, we return the entropy rounded to the indicated decimals.
        return round(entropy, decimals)

    # This static method calculates necessary decryption time to crack a password (in years) in a brute-force attack.
    @staticmethod
    def calculate_decryption_time(entropy: Union[int, float],
                                  decimals: int = 2, attempts_per_second=1e12) -> Union[int, float]:

        # This ensures entropy provided is a number.
        if not isinstance(entropy, Union[int, float]):

            raise TypeError('entropy must be a number')

        # This ensures the number of decimals required is an integer.
        if not isinstance(decimals, int):

            raise TypeError('Number of decimals must be an integer')

        # This ensures the number of decimals required is greater than or equal to 0.
        if decimals < 0:

            raise ValueError('Number of decimals cannot be a negative integer')

        # This ensures attempts per second is a number.
        if not isinstance(attempts_per_second, Union[int, float]):

            raise TypeError('attempts per second must be an integer')

        # This ensures attempts per second is a positive number.
        if attempts_per_second <= 0:

            raise ValueError('attempts per second must be a positive integer')

        # Seconds per year = 60 seconds * 60 minutes * 24 hours * 365 days.
        seconds_per_year = 60 * 60 * 24 * 365

        # These are all the possible combinations of the password,
        # therefore, all the possible attempts to crack it.
        combinations = 2 ** entropy

        # T = 2^H / V * S
        decryption_time_in_years = combinations / (attempts_per_second * seconds_per_year)

        # If decryption time in years is an integer:
        if isinstance(decryption_time_in_years, int):

            return decryption_time_in_years

        # If the condition above is not met, and if the number of decimals provided is 0, round to an integer:
        if decimals == 0:

            return round(decryption_time_in_years)

        # Finally, we return the time rounded to the provided decimals.
        return float(f'{decryption_time_in_years:.{decimals}e}')

    # Call the 3 methods of the class to create their respective attributes.
    def create_password(self):

        try:

            # Generates the password.
            generated_password = self.generate_password(self.length)

            # Calculates its entropy.
            entropy_of_password = self.calculate_entropy(generated_password)

            # Calculates the time to decrypt it.
            decryption_password_time = self.calculate_decryption_time(entropy_of_password)

            # Returns each variable created above.
            return generated_password, entropy_of_password, decryption_password_time

        # If an error happens, this will handle it.
        except Exception as exception:

            print(f'There was an error: {exception}')

            # Returns None for each variable respectively
            return None, None, None

    # For printing the object.
    def __str__(self):

        return ('Generator(' +
                f'length={self.length}, ' +
                f'password={self.password}, ' +
                f'entropy={self.entropy}, ' +
                f'decryption_time={self.decryption_time})'
                )
