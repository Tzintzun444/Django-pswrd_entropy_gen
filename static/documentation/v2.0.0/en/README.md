# PSWRD_ENTROPY_GEN PROJECT
This project is a simple but powerful tool to create secure passwords based on **entropy** \(information theory).

## Description
This is a password generator based on entropy in bits, this means that the passwords created can be measured on
how much is possible to crack the password based on its randomness, and can calculate how much time it would need to be decrypted.
The generator is a class called 'Generator' \(of course) and has 4 methods involved, which we will see later.

## Installation

To install the package, you only need to use the following command:
```bash
pip install pswrd_entropy_gen
```

Once the package has been installed, import its class "Generator":

```python
from pswrd_entropy_gen.generator import Generator
```

## Characteristics

### Class Generator:

The class 'Generator' 3 static methods and 1 instance method:

+ generate_password\() static method.

+ calculate_entropy\() static method.

+ calculate_decryption_time\() static method.

+ create_password\() instance method.

Class 'Generator' creates a password based on the length provided, it receives as a parameter the required length 
\(integer) of the password, then it creates the password and will return 3 variables: First, the 'password', 
which is the password that was created. Second, the 'entropy' as its name says, it is the entropy 
related to the password. And finally, the 'decryption_time' that is the time required to crack the 
password by brute force attack \(theoretically):

```python
class Generator:
    
    # The class is initialized with the length of the password as an attribute.
    # The other attributes are given by the create_password method.
    def __init__(self, length):

        # This is the length of the password.
        self._length = length

        # These are the password, its entropy and the time to decrypt it.
        (self._password, self._entropy,
         self._decryption_time) = self.create_password()
```

### create_password() instance method:

This is the general method of the class, it uses the other 3 methods to create a password, calculate its entropy in 
bits and finally calculate how much time is necessary to crack the password.

```python
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
```

### generate_password() static method:

The method generates a secure password based on entropy, it ensures that is cryptographically secure and hard to crack,
while more characters in the password, security grows.

The method has 6 parameters:

+ length:
It is the length of the password, it must be a positive integer \(do not exist decimal or negative passwords), 
it is recommended to be 8 or greater numbers. It is not defined by default.

+ use_uppercase:
It is a boolean value, it is true by default. This means that is allowed to have at least 1 uppercase letter in
the password, it may be more than 1.

+ use_numbers:
Also is a boolean value, true by default. Also means that is allowed to have at least 1 number \(0-9) in the 
password, it may be more than 1.

+ use_punctuations:
This is a boolean value, true by default. Includes at least 1 punctuation character \(#$%/! for example)
in the password, also it may be more than 1.

+ customized:
It is a string, al character in the string will be in the password mandatory, it would be a string with unique 
characters, but if a character is duplicated, will be fixed in the class.

+ not_allowed:
Finally, this is a string that contains all characters that will not be in the password, also if there is a duplicated 
character, will be fixed. If you have a character in the customized and not allowed characters simultaneously, an error
will be raised, avoid it.

The method uses the 'string' and 'secrets' modules for its functionality. The use of at least 1 lowercase letter is 
mandatory, and all parameters by default are in the 'situations' dictionary with their respective characters as a
value.

Firstly, the 'password' list is initialized, it will store the characters of the password that will be used later. 
Also, a dictionary stores each situation and its respectively characters by default. 
Additionally, the 'characters' variable will store all the characters available for using in the password, and it is 
initialized with all the lowercase letters by default.
 
```python
    # This class method generates a password based on the characters allowed and the provided length.
    @staticmethod
    def generate_password(length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True,
                          not_allowed='', customized='') -> str:

        # This is the list that stores the characters of the password.
        password = []
        
        # These are all the default optional characters for the password.
        punctuation_characters = '!#$%&*+_-/'
        type_of_characters = {
            # ABCDEFGHIJKLMNOPQRSTUVWXYZ
            'uppercase': string.ascii_uppercase,
            # 1234567890
            'numbers': string.digits,
            # !#$%&*+_-/
            'punctuations': punctuation_characters
        }
        
        # abcdefghijklmnopqrstuvwxyz
        characters = string.ascii_lowercase
```

After that, there are some validations for parameters, such as 'length' is a positive integer, or 'use_uppercase', 
'use_numbers' and 'use_punctuations' are boolean values.

```python
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
```

Next, if the 'customized' parameter is provided, this validates that is a string. After that, duplicated characters
are deleted and the remaining characters are added in the 'password' list.

```python
        # If custom characters are provided:
        if customized:

            # This ensures the custom characters are a string.
            if not isinstance(customized, str):

                raise TypeError('Customized characters must be a string')

            # This deletes duplicated characters in the custom characters.
            customized = set(customized)

            # This adds the custom characters in the password list.
            password.extend(list(customized))
```

These validations are done with 'not_allowed' characters too, this ensures that 'not_allowed' is a string, and if 
'customized' characters are provided, this ensures that there are no characters crashing with each other. Finally, 
if all characters in 'not_allowed' are the same of any situation \(for example, '1234567890' has the same characters of 
'0123456789'), an error will be raised.


```python
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
```

If all validations are passed, then each character of 'not_allowed' will be used for check if the character is in any 
situation and will remove it. If the character is not in a situation, does not do anything.

```python
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
```

After that, the parameter of each optional situation and their respectively characters \(without not allowed characters) 
are stored in a dictionary as values, and appends a lowercase letter in the password.
 

```python
        # This stores the situations in a dictionary as the key, amd their boolean values and the characters related
        # as the values.
        situations = {'uppercase': (use_uppercase, type_of_characters['uppercase']),
                      'numbers': (use_numbers, type_of_characters['numbers']),
                      'punctuations': (use_punctuations, type_of_characters['punctuations']),
                      }

        # This appends a random character from the default (or the characters available if any character was deleted).
        password.append(secrets.choice(characters))
```

Next a for loop adds 1 character of each of the character types if those are 'True' in the parameters above, 
this ensures that at least 1 of each type was added.
```python
        # The for loop checks if the situations are True or false.
        for character_type in situations.values():
    
            if character_type[0]:
                
                # If the situation is allowed (or its parameter is True) adds the specified characters as possibles for the
                # password.
                characters += character_type[1]
                
                # Also adds 1 character of each type allowed to ensure that there is at least 1.
                password.append(secrets.choice(character_type[1]))
```

After that, the length remaining is calculated, if 'remaining' is negative, means that probably 'customized' string had 
more characters than the possibles \(for example, length of the password should be equal to 5, but 
customized='asf23842jw'), and then an error will be raised. If remaining is positive means that the password still 
needs characters, given that, the 'random_password' list will store the remaining characters needed to complete the 
password, and finally, with a list comprehension, the necessary characters are chosen and added in a list, 
which is joined with our 'password' list.

```python
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
```

Finally, when the process above is finished \(or 'remaining' is equal to 0, that means password is completed), 
the characters in the list are randomly shuffled and joined as a string.

```python
        # If remaining equals to 0 means that password has been completed.
        # The 'password' list is shuffled for avoid patterns.
        secrets.SystemRandom().shuffle(password)

        # Finally, the shuffled characters are joined in a string.
        final_password = ''.join(password)

        # Returns the secure password.
        return final_password
```

And the password is returned. Woohoo!

### calculate_entropy() static method:

The method calculates the entropy in bits of the password, this is useful for calculate the decryption time of the
password and also shows how much secure is the password. The method uses the 'math' module to use the logarithm base 2. 

The method has 2 parameters:

+ password:
This is the password created \(or it can be any password), it must be a string.  

+ decimals:
This parameter defines how many decimals there will be in the entropy \(and if it is necessary, round the entropy to 
that number of decimals). By default, there is 1 decimal.

```python
    # This method calculates the entropy of the provided password.
    @staticmethod
    def calculate_entropy(password: str, decimals: int = 1) -> Union[int, float]:
```

Before the method starts, we validate the parameters, and if an error was not raised, then we continue.

```python
        # This ensures the password provided is a string.
        if not isinstance(password, str):

            raise TypeError('password must be a string')

        # This ensures the number of decimals required is an integer.
        if not isinstance(decimals, int):

            raise TypeError('The number of decimals must be an integer')

        # This ensures the number of decimals required is greater than or equal to 0.
        if decimals < 0:

            raise ValueError('The number of decimals must be a positive integer')
```

First, all characters are stored in a set for avoid repetitive characters, also we need to calculate the length of
the password. And finally we initialize the variable 'argument_log' as 0.

```python
        # The set ensures that we don't take repetitive characters.
        unique_characters = set(password)
        
        # Calculates the length of the password.
        length_password = len(password)
        
        # Initialize the argument of the log base 2.
        argument_log = 0
```

Next, the character types are stored again in a dictionary called 'situations', the key is the situation and
the values are the characters and the number of possibilities for each type.

```python
        # The dictionary stores the possible characters and the number of them.
        situations = {'uppercase': (string.ascii_uppercase, len(string.ascii_uppercase)),
                      # ABCDEFGHIJKLMNOPQRSTUVWXYZ
                      'lowercase': (string.ascii_lowercase, len(string.ascii_lowercase)),
                      # abcdefghijklmnopqrstuvwxyz
                      'numbers': (string.digits, len(string.digits)),
                      # 1234567890
                      'punctuations': ('!#$%&*+_-/', len('!#$%&*+_-/')),
                      # !#$%&*+_-/
                      }
```

We use a for loop to verify if 1 \(or more, but only need 1 for this verification) character of each type is in the 
password, and if it is, we add to the argument the number of possible characters of the type.

```python
        # Separates the characters from the number of possible characters.
        for character_type, possibilities in situations.values():
            
            # Checks that a character of the specified type appears at least once,
            # this means that the character type is allowed in the password.
            if any(character in character_type for character in unique_characters):
                
                # If it is true, sums the number of possible characters to the argument of the log.
                argument_log += possibilities
```

Finally, we calculate entropy using the next formula, where:

![Entropy formula](entropy_formula.png)

+ H: Represents the password entropy.

+ L: Represents the password length.

+ n: Represents the total possibilities for each character in the password.

```python
        # Using the previous formula, we calculate its entropy and we verify the formula is not empty.
        entropy = length_password * math.log2(argument_log) if length_password > 0 else 0
```

Now, if entropy is already an integer, return it, if it is not, but the 'decimals' parameter is equal to 0, entropy is 
rounded to an integer. Finally, if the conditions before are False, entropy is rounded to the provided decimals.

````python
        # If entropy is already an integer:
        if isinstance(entropy, int):

            return entropy

        # If the entropy must not have decimals, round to an integer:
        if decimals == 0:

            return round(entropy)

        # Finally, we return the entropy rounded to the indicated decimals.
        return round(entropy, decimals)
````

And that's all!

### calculate_decryption_time static method:

The function calculates how much time a hacker would need \(theoretically) to crack the password, this shows the 
security involved in the password and indicates if it's a good idea to use the password. 

The function has 3 parameters:

+ entropy:
This is the password entropy, it is needed to calculate how many attempts are necessary to crack the password in a 
brute force attack, if the entropy is bigger, the necessary attempts will be too. It must be a positive number.

+ decimals:
This defines how many decimals there will be in the time to decrypt the password \(in years). By default, there will be
2 decimals in the time. It must be a positive integer.

+ attempts_per_second:
This is the number of attempts that a hacker can make per second in a brute force attack \(obviously, this is relative),
but we define it as 1*10^12 attempts per second by default. It must be a positive integer.

```python
    # This method calculates the necessary decryption time to crack a password (in years) in a brute-force attack.
    @staticmethod
    def calculate_decryption_time(entropy: Union[int, float],
                                  decimals: int = 2, 
                                  attempts_per_second: Union[int, float] = 1e12) -> Union[int, float]:
```

Before starting, we validate the parameters, if every thing is correct, we continue.

```python
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
```

First, we calculate how many seconds are in a year.

```python
        # Seconds per year = 60 seconds * 60 minutes * 24 hours * 365 days.
        seconds_per_year = 60 * 60 * 24 * 365
```

After that, we calculate how many combinations are possible with the entropy received.

```python
        # These are all the possible combinations of the password, 
        # therefore, all the possible attempts to crack it.
        combinations = 2 ** entropy
```

Next, we calculate the decryption time based on the following formula, where:

![Decryption_time_formula](decryption_time_formula.png)

+ T: Represents the decryption time in years.

+ H: Represents the password entropy.

+ V: Represents the attempts per second that a hacker can make.

+ S: Represents the seconds in 1 year.

```python
        # T = 2^H / V * S
        decryption_time_in_years = combinations / (attempts_per_second * seconds_per_year)
```

Now, if decryption_time is already an integer, return it, if it is not, but the 'decimals' parameter is equal to 0, it is 
rounded to an integer. Finally, if the conditions before are False, it is rounded to the provided decimals.

```python
        # If decryption time in years is an integer:
        if isinstance(decryption_time_in_years, int):

            return decryption_time_in_years

        # If the condition above is not met, and if the number of decimals provided is 0, round to an integer:
        if decimals == 0:

            return round(decryption_time_in_years)

        # Finally, we return the time rounded to the provided decimals.
        return float(f'{decryption_time_in_years:.{decimals}e}')
```

We've finished!

## Examples

### create_password() instance method:

+ Default use:

  In this case, we will use the default performance of the method \(this means all types of characters are allowed), 
  we need a password with 12 characters:
  
```python
# The password length is 12 characters
pswrd_generator = Generator.create_password(12)
# output: UbMlRi/N5+4, 78.7, 15568.76
```

### generate_password() static method:

All the following passwords will have 18 characters.

+ Default use:

  As we saw before, we will generate the password with the default performance of the method.
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18)
# output: +1ND%q#h2tOC-4_F$8 
```

+ Password without punctuation:

  Now, the password does not allow punctuation characters \(or, as the same way, lower and uppercase letters and 
  digits are allowed):
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18, use_punctuations=False)
# output: 6dVf1UKHUHOq0RSEUL 
```

+ Password without digits:

  Now, the password does not allow digits \(or, as the same way, lower and uppercase letters and 
  punctuation characters are allowed):
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18, use_numbers=False)
# output: vf/CE_uu!W&#Sw%jhD 
```

+ Password without uppercase letters:

  Now, the password does not allow uppercase letters \(or, as the same way, lowercase letters, digits and 
  punctuation characters are allowed):
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18, use_uppercase=False)
# output: /3_4!#&u991_43-m4t
```

+ Password with only lowercase letters: 

  Finally, the password only allows lowercase letters:
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18, use_uppercase=False, 
                                                 use_punctuations=False, use_numbers=False)
# output: ytvyyzlfnamurebtoh
```

+ Combined situations: 

  In this case, the password allows lowercase letters and digits, but does not allow uppercase letters
  and punctuation characters:
  
```python
# This is the needed password.
generated_password = Generator.generate_password(18, use_uppercase=False, 
                                                 use_punctuations=False)
# output: ou0h92pj1cwqe8ny02
```

+ Password with uppercase and lowercase letters, digits and punctuations, customized and not_allowed characters:

  In this final case, the password allow all type of characters, but sets some specific characters and disallow others:
  
```python
# This is the needed password.
generated_password = Generator.generate_password(12, use_uppercase=True, use_numbers=True, use_punctuations=True,
                                                 customized='t4zA7', not_allowed='129685dfg/-'
                                                 )
# output: Qy4A&PZ3t0z7
# As you can see, each character of customized is in the password at least once, and all characters in not allowed 
# are not in the password.
```

### calculate_entropy() static method:

We will use the passwords generated above for these examples.

+ Default use:
  
  This is the entropy of the password with all types of characters:

```python
# This is the entropy of the password: +1ND%q#h2tOC-4_F$8
entropy = Generator.calculate_entropy("+1ND%q#h2tOC-4_F$8")
# output: 118.0
```

+ Password without punctuation:

  This is the entropy of the password without punctuation characters:

```python
# This is the entropy of the password: 6dVf1UKHUHOq0RSEUL
entropy = Generator.calculate_entropy("6dVf1UKHUHOq0RSEUL")
# output: 107.2
```

+ Password without digits:

  This is the entropy of the password without digits:

```python
# This is the entropy of the password: vf/CE_uu!W&#Sw%jhD
entropy = Generator.calculate_entropy("vf/CE_uu!W&#Sw%jhD")
# output: 115.1
```

+ Password without uppercase letters:

  This is the entropy of the password without uppercase letters:

```python
# This is the entropy of the password: /3_4!#&u991_43-m4t
entropy = Generator.calculate_entropy("/3_4!#&u991_43-m4t")
# output: 109.6
```

+ Password with only lowercase letters: 

  This is the entropy of the password with only lowercase letters:

```python
# This is the entropy of the password: ytvyyzlfnamurebtoh
entropy = Generator.calculate_entropy("ytvyyzlfnamurebtoh")
# output: 84.6
```
  
+ Combined situations:

  Finally, this is the entropy of the password with lowercase letters and digits allowed:

```python
# This is the entropy of the password: ou0h92pj1cwqe8ny0
generated_password = Generator.calculate_entropy('ou0h92pj1cwqe8ny02')
# output: 93.1
```

The entropy of each password is used to calculate its security in a brute force attack.

### calculate_decryption_time() static method:

Again, we will use the passwords and their entropies generated above for these examples. The time calculated is only
theoretical and is a metric of password security in a brute-force attack:

+ Default use:
  
  This is the necessary decryption time \(in years) to crack the password with all types of characters:

```python
# This is the decryption time of the password: +1ND%q#h2tOC-4_F$8
# Its entropy is 118.0
decryption_password_time = Generator.calculate_decryption_time(118.0)
# output: 1.05e+16
```

+ Password without punctuation:

  This is the necessary decryption time \(in years) to crack the password without punctuation characters:

```python
# This is the decryption time of the password: 6dVf1UKHUHOq0RSEUL
# Its entropy is 107.2
decryption_password_time = Generator.calculate_decryption_time(107.2)
# output: 5910000000000.0
```

+ Password without digits:

  This is the necessary decryption time \(in years) to crack the password without digits:

```python
# This is the decryption time of the password: vf/CE_uu!W&#Sw%jhD
# Its entropy is 115.1
decryption_password_time = Generator.calculate_decryption_time(115.1)
# output: 1410000000000000.0
```

+ Password without uppercase letters:

  This is the necessary decryption time \(in years) to crack the password without uppercase letters:

```python
# This is the decryption time of the password: /3_4!#&u991_43-m4t
# Its entropy is 109.6
decryption_password_time = Generator.calculate_decryption_time(109.6)
# output: 1410000000000000.0
```

+ Password with only lowercase letters: 

  This is the necessary decryption time \(in years) to crack the password only with uppercase letters:

```python
# This is the entropy of the password: ytvyyzlfnamurebtoh
# Its entropy is 84.6
decryption_password_time = Generator.calculate_decryption_time(109.6)
# output: 31200000000000.0
```
  
+ Combined situations:

  Finally, this is the necessary decryption time \(in years) to crack the password with lowercase letters and 
  digits allowed:

```python
# This is the entropy of the password: ou0h92pj1cwqe8ny02
# Its entropy is 93.1
decryption_password_time = Generator.calculate_decryption_time(93.1)
# output: 337000000.0
```

## Contributions

I'm open and happy to receive any input or contribution to the project. You can submit a pull request, 
report a bug, and add new features without any problems!

## License

This project was made under the MIT license:
[MIT License](https://github.com/Tzintzun444/pswrd_entropy_gen/blob/main/pswrd_entropy_gen/LICENSE.txt)

## Credits

+ Author: Alfredo Tzintzun.

+  Libraries used:
    - secrets.
    - string.
    - math.
    - typing.

I hope you enjoy this project!
