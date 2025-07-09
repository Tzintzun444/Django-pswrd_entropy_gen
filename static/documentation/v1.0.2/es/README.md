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

The class 'Generator' has 3 static methods and 1 instance method:
+ generate_password\() static method.
+ calculate_entropy\() static method.
+ calculate_decryption_time\() static method.
+ create_password\() instance method.

Class 'Generator' creates a password based on the length provided, it receives as a parameter the required length 
\(integer)of the password, then it creates the password and will return 3 variables: First, the 'generated_password', 
which is the password that was created. Second, the 'entropy_of_password' as its name says, it is the entropy 
related to the password. And finally, the 'decryption_password_time' that is the time required to crack the 
password by brute force attack \(theoretically):

```python
class Generator:
    
    # The class receives the length of the password as an attribute.
    # The other attributes are given by the create_password method.
    def __init__(self, length):
        
        # This is the length of the password.
        self._length = length
        
        # These are the password, its entropy and the time to decrypt it.
        (self._generated_password, self._entropy_of_password,
         self._decryption_password_time) = self.create_password()
```

### create_password() instance method:

This is the main method of the class, it uses the other 3 methods to create a password, calculate its entropy in 
bits and finally calculate how much time is necessary to crack the password.

```python
    
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
            
            # This is the message error.
            return f'There was an error: {exception}'
```

### generate_password() static method:

The method generates a secure password based on entropy, it ensures that is cryptographically secure and hard to crack,
while more characters in the password, security grows.

The method has 4 parameters:
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
And finally, it is a boolean value, true by default. Includes at least 1 punctuation character \(.#$%/! for example)
in the password, also it may be more than 1.

The method uses the 'string' and 'secrets' modules for its functionality. The use of lowercase letters is 
mandatory, and all parameters by default are in the 'situations' dictionary with their respective characters as a
value.

 
```python
    # This method generates a password based on the characters allowed and the provided length.
    @staticmethod
    def generate_password(length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True) -> str:
        
        # Ensure that length is a positive integer.
        if length <= 0:
          
            # Message error. 
            raise ValueError('The number must be a positive integer')
        
        # Select the default lowercase characters in the 'characters' variable that contains all the possible characters
        characters = string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
        
        # Stores the situations in a dictionary as the key, amd their boolean values and the characters related
        # as the values.
        
        situations = {'uppercase': (use_uppercase, string.ascii_uppercase), # True, ABCDEFGHIJKLMNOPQRSTUVWXYZ
                      'numbers': (use_numbers, string.digits), # True, 0123456789
                      'punctuations': (use_punctuations, string.punctuation), # True, !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                      }
```

Next, creates the 'password' list, here will be stored all characters of the password. Then, a for loop adds 1 
character of each of the character types if those are 'True' in the parameters above, this ensures that at least
1 of each type was added.

```python
        # This is the list that stores the characters of the password.
        password = []
        
        # The for loop checks if the situations are True or false.
        for character_type in situations.values():
    
            if character_type[0]:
                
                # If the situation is allowed (or its parameter is True) adds the specified characters as possibles for the
                # password.
                characters += character_type[1]
                
                # Also adds 1 character of each type allowed to ensure that there is at least 1.
                password.append(secrets.choice(character_type[1]))
```

After that, the length remaining is calculated and with a list comprehension, the necessary characters are chosen 
and added in a list, which is joined with our 'password' list.

```python
        # This is the necessary length to complete the password.
        remaining = length - len(password)
        
        # Selects all necessary characters to complete the password
        random_password = [secrets.choice(characters) for _ in range(remaining)]
        
        # Extends the original 'password' list with the list above.
        password.extend(random_password)
```

Finally, the characters in the list are randomly shuffled and joined as a string.

```python
        # The 'password' list is shuffled for avoid patterns
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
        situations = {'uppercase': (string.ascii_uppercase, 26), # ABCDEFGHIJKLMNOPQRSTUVWXYZ, 26
                      'lowercase': (string.ascii_lowercase, 26), # abcdefghijklmnopqrstuvwxyz, 26
                      'numbers': (string.digits, 10), # 0123456789, 10
                      'punctuations': (string.punctuation, 32), # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~, 32
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

![Entropy formula](https://github.com/Tzintzun444/pswrd_entropy_gen/blob/images/entropy_formula.png)

+ H: Represents the password entropy.
+ L: Represents the password length.
+ n: Represents the total possibilities for each character in the password.

And return the entropy rounded to the defined decimals at the beginning of the method.

```python
        # Using the previous formula, we calculate its entropy and we verify the formula is not empty.
        entropy = length_password * math.log2(argument_log) if length_password > 0 else 0
        
        # Finally, we return the entropy rounded to the indicated decimals.
        return round(entropy, decimals)
```

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
                                  decimals: int = 2, attempts_per_second=1e12) -> Union[int, float]:
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

![Decryption_time_formula](https://github.com/Tzintzun444/pswrd_entropy_gen/blob/images/decryption_time_formula.png)

+ T: Represents the decryption time in years.
+ H: Represents the password entropy.
+ V: Represents the attempts per second that a hacker can make.
+ S: Represents the seconds in 1 year.

```python
        # T = 2^H / V * S
        decryption_time_in_years = combinations / (attempts_per_second * seconds_per_year)
```

Finally, we return the time rounded to the indicated decimals at the beginning of the method.

```python
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
  pswrd_generator = Generator.create_password(12) # The password length is 12 characters
  # output: UbMlRi^N5)4, 78.7, 15568.76
  ```

### generate_password() static method:

All the following passwords will have 18 characters.

+ Default use:

  As we saw before, we will generate the password with the default performance of the method.
  
  ```python
  # This is the needed password.
  generated_password = Generator.generate_password(18)
  # output: `1ND%q#h2tOC:4'F]8 
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
  # output: vf?CE'uu;W&~Sw^jhD 
  ```

+ Password without uppercase letters:

  Now, the password does not allow uppercase letters \(or, as the same way, lowercase letters, digits and 
  punctuation characters are allowed):
  
  ```python
  # This is the needed password.
  generated_password = Generator.generate_password(18, use_uppercase=False)
  # output: &3_4]}[u991!43+m4t
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

### calculate_entropy() static method:

We will use the passwords generated above for these examples.

+ Default use:
  
  This is the entropy of the password with all types of characters:

  ```python
  # This is the entropy of the password: `1ND%q#h2tOC:4'F]8
  entropy = Generator.calculate_entropy("`1ND%q#h2tOC:4'F]8")
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
  # This is the entropy of the password: vf?CE'uu;W&~Sw^jhD
  entropy = Generator.calculate_entropy("vf?CE'uu;W&~Sw^jhD")
  # output: 115.1
  ```

+ Password without uppercase letters:

  This is the entropy of the password without uppercase letters:

  ```python
  # This is the entropy of the password: &3_4]}[u991!43+m4t
  entropy = Generator.calculate_entropy("&3_4]}[u991!43+m4t")
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
  # This is the decryption time of the password: `1ND%q#h2tOC:4'F]8
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
  # This is the decryption time of the password: vf?CE'uu;W&~Sw^jhD
  # Its entropy is 115.1
  decryption_password_time = Generator.calculate_decryption_time(115.1)
  # output: 1410000000000000.0
  ```

+ Password without uppercase letters:

  This is the necessary decryption time \(in years) to crack the password without uppercase letters:

  ```python
  # This is the decryption time of the password: &3_4]}[u991!43+m4t
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
[MIT License](https://github.com/Tzintzun444/pswrd_entropy_gen/blob/write-readme/pswrd_entropy_gen/LICENSE.txt)

## Credits

+ Author: Alfredo Tzintzun.

+ External libraries used:
    - secrets.
    - string.
    - math.
    - typing.

I hope you enjoy this project!