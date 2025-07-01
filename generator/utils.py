import math
import secrets
import string
from typing import Union


# This is the main class
class Generator:

    punctuation_characters = '!#$%&*+_-/'
    type_of_characters = {
        'default': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'numbers': string.digits,
        'punctuations': punctuation_characters
    }

    # The class receives the length of the password as an attribute.
    # The other attributes are given by the create_password method.
    def __init__(self, length):

        # This is the length of the password.
        self._length = length

        # These are the password, its entropy and the time to decrypt it.
        (self._generated_password, self._entropy_of_password,
         self._decryption_password_time) = self.create_password()

    @property
    def length(self):

        return self._length

    @length.setter
    def length(self, length):

        self._length = length

    @property
    def generated_password(self):

        return self._generated_password

    @generated_password.setter
    def generated_password(self, generated_password):

        self._generated_password = generated_password

    @property
    def entropy_of_password(self):

        return self._entropy_of_password

    @entropy_of_password.setter
    def entropy_of_password(self, entropy_of_password):

        self._entropy_of_password = entropy_of_password

    @property
    def decryption_password_time(self):

        return self._decryption_password_time

    @decryption_password_time.setter
    def decryption_password_time(self, decryption_password_time):

        self._decryption_password_time = decryption_password_time

    # This method generates a password based on the characters allowed and the provided length.
    @classmethod
    def generate_password(cls, length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True,
                          not_allowed=None, customized=None) -> str:

        if not_allowed:

            not_allowed = {not_allowed}

        # Ensure that length is a positive integer.
        if length <= 0:

            # Message error.
            raise ValueError('The number must be a positive integer')

        if not_allowed:

            for situation, characters in cls.type_of_characters.items():

                for letter in not_allowed:

                    if letter in characters:

                        cls.type_of_characters[situation] = characters.replace(letter, '')

        # Stores the situations in a dictionary as the key, amd their boolean values and the characters related
        # as the values.
        situations = {'uppercase': (use_uppercase, cls.type_of_characters['uppercase']),  # True, ABCDEFGHIJKLMNOPQRSTUVWXYZ
                      'numbers': (use_numbers, cls.type_of_characters['numbers']),  # True, 0123456789
                      'punctuations': (use_punctuations, cls.type_of_characters['punctuations']),
                      # True, !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                      }

        # This is the list that stores the characters of the password.
        password = []
        characters = cls.type_of_characters['default']

        # The for loop checks if the situations are True or false.
        for character_type in situations.values():

            if character_type[0]:

                # If the situation is allowed (or its parameter is True) adds the specified characters as
                # possibles for the password.
                characters += character_type[1]

                # Also adds 1 character of each type allowed to ensure that there is at least 1.
                password.append(secrets.choice(character_type[1]))

        if customized:

            password.extend(list(customized))

        # This is the necessary length to complete the password.
        remaining = length - len(password)

        # Selects all necessary characters to complete the password
        random_password = [secrets.choice(characters) for _ in range(remaining)]

        # Extends the original 'password' list with the list above.
        password.extend(random_password)

        # The 'password' list is shuffled for avoid patterns
        secrets.SystemRandom().shuffle(password)

        # Finally, the shuffled characters are joined in a string.
        final_password = ''.join(password)

        # Returns the secure password.
        return final_password

    # This method calculates the entropy of the provided password.
    @classmethod
    def calculate_entropy(cls, password: str, decimals: int = 1) -> Union[int, float]:

        # The set ensures that we don't take repetitive characters.
        unique_characters = set(password)

        # Calculates the length of the password.
        length_password = len(password)

        # Initialize the argument of the log base 2.
        argument_log = 0

        # The dictionary stores the possible characters and the number of them.
        situations = {'uppercase': (cls.type_of_characters['uppercase'], len(cls.type_of_characters['uppercase'])),  # ABCDEFGHIJKLMNOPQRSTUVWXYZ, 26
                      'lowercase': (cls.type_of_characters['default'], len(cls.type_of_characters['default'])),  # abcdefghijklmnopqrstuvwxyz, 26
                      'numbers': (cls.type_of_characters['numbers'], len(cls.type_of_characters['numbers'])),  # 0123456789, 10
                      'punctuations': (cls.type_of_characters['punctuations'], len(cls.type_of_characters['punctuations'])),  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~, 32
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

        # Finally, we return the entropy rounded to the indicated decimals.
        return round(entropy, decimals)

    # This method calculates the necessary decryption time to crack a password (in years) in a brute-force attack.
    @staticmethod
    def calculate_decryption_time(entropy: Union[int, float],
                                  decimals: int = 2, attempts_per_second=1e12) -> Union[int, float]:

        # Seconds per year = 60 seconds * 60 minutes * 24 hours * 365 days.
        seconds_per_year = 60 * 60 * 24 * 365

        # These are all the possible combinations of the password,
        # therefore, all the possible attempts to crack it.
        combinations = 2 ** entropy

        # T = 2^H / V * S
        decryption_time_in_years = combinations / (attempts_per_second * seconds_per_year)

        # Finally, we return the time rounded to the provided decimals.
        return float(f'{decryption_time_in_years:.{decimals}e}')

    # Call the 3 static methods of the class to create their respective attributes.
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
            # This is the message error.
            return None, None, None

    # For printing the object.
    def __str__(self):

        return (f'The password generated is: {self.generated_password}\n'
                f'Entropy={self.entropy_of_password}\n'
                f'The time necessary to decrypt it is {self.decryption_password_time} years')
