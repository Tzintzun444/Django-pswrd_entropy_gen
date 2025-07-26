# PROYECTO PSWRD_ENTROPY_GEN 
Este proyecto es una simple pero poderosa herramienta para crear contraseñas seguras basadas en la **entropía** \(Teoría de la información).

## Descripción
Esto es un generador de contraseñas basado en la entropía en bits, esto quiere decir que las contraseñas creadas pueden 
ser medidas con base en qué tan posible es comprometer la contraseña basada en su aleatoriedad, y puede calcular cuánto 
tiempo se necesitaría para ser descifrada. 
El generador es una clase llamada 'Generator' \(por supuesto) y tiene 4 métodos involucrados, los cuales veremos después.

## Instalación
Para instalar el paquete, solo necesitas usar el siguiente comando:

```bash
pip install pswrd_entropy_gen
```

Una vez el paquete ha sido instalado, importa su clase "Generator":

```python
from pswrd_entropy_gen.generator import Generator
```

## Características

### Clase Generator:

La clase 'Generator' tiene 3 métodos estáticos y 1 método de instancia

+ método estático generate_password\().

+ método estático calculate_entropy\().

+ método estático calculate_decryption_time\().

+ método de instancia create_password\().

La clase 'Generator' crea una contraseña basada en la longitud dada, recibe como un parametro a la longitud requerida 
\(número entero) de la contraseña, después crea la contraseña y retornará 3 variables: Primero, el atributo 'generated_password', 
el cual es la contraseña que fue creada. Después, el atributo 'entropy_of_password' y como dice su nombre \(en inglés), es 
la entropía relacionada a la contraseña. Y finalmente, el atributo 'decryption_password_time' que es el tiempo requerido 
para comprometer la contraseña durante un ataque de fuerza bruta \(teóricamente hablando).

```python
class Generator:
  
    # La clase recibe la longitud de la contraseña como un atributo.
    # Los otros atributos son dados por el método create_password.
    def __init__(self, length):
        
        # Esta es la longitud de la contraseña.
        self._length = length
        
        # Estos son la contraseña, su entropía y el tiempo para descifrarla.
        (self._password, self._entropy,
         self._decryption_time) = self.create_password()
```

### Método de instancia create_password():

Este es el método principal de la clase, usa los otros 3 métodos para crear la contraseña, calcula su entropía en bits y 
finalmente calcula cuánto tiempo es necesario para comprometer la contraseña.

```python
    # Llama a los 3 métodos estáticos de la clase para crear sus respectivos atributos.
    def create_password(self):

        try:

            # Genera la contraseña.
            generated_password = self.generate_password(self.length)

            # Calcula su entropía.
            entropy_of_password = self.calculate_entropy(generated_password)

            # Calcula el tiempo para descifrarla.
            decryption_password_time = self.calculate_decryption_time(entropy_of_password)

            # Retorna cada variable creada arriba.
            return generated_password, entropy_of_password, decryption_password_time

        # Si ocurre un error, esto lo manejará.
        except Exception as exception:

            print(f'There was an error: {exception}')
            
            # Retorna None para cada variable respectivamente.
            return None, None, None
```

### Método estático generate_password():

El método genera una contraseña segura basada en entropía, asegura que es criptográficametne segura y difícil de comprometer, 
mientras más characteres en la contraseña, la seguridad aumenta.

El método tiene 4 parámetros

+ length:
Es la longitud de la contraseña, debe ser un número entero positivo \(no existen contraseñas decimales o negativas), es 
recomendado que sea de 8 o más números. No está definida por defecto.

+ use_uppercase:
Es un valor booleano, es true por defecto. Esto significa que está permitido tener al menos 1 letra mayúscula en la 
contraseña, puede ser más de 1.

+ use_numbers:
También es un valor booleano, true por defecto. También significa que está permitido tener al menos 1 número \(0-9) en 
la contraseña, puede ser más de 1.

+ use_punctuations:
Este es un valor booleano, true por defecto. Incluye al menos 1 caractter de puntuación \(#$%/! por ejemplo) en la 
contraseña, también puede ser más de uno.

+ customized:
Es una cadena, todos los caracteres en la cadena estarán en la contraseña obligatoriamente, debería ser una cadena con 
caracteres únicos, pero si un caracter es duplicado, será arreglado en la clase.

+ not_allowed:
Finalmente, este es una cadena que contiene todos los caracteres que no estarán en la contraseña, also si hay un 
caracter duplicado, será arreglado. Si tienes un caracter en 'customized' y 'not_allowed' al mismo tiempo, habrá un 
error, evítalo.

El método usa los módulos de 'string' y 'secrets' para su funcionamiento. El uso de letras minúsculas es obligatorio, y 
todos los parámetros por defecto están en el diccionario llamado 'situations' con sus respectivos caracteres como valor.

Inicialmente, la lista 'password' se inicializa, guardará los caracteres de la contraseña que serán usados después. 
También un diccionario guarda cada situación y sus respectivos caracteres por defecto. Adicionalmente, la variable 
'characters' almacenará todos los caracteres disponibles para usar en la contraseña, y es inicializada con todas las 
letras minúsculas por defecto.
 
```python
    # Este método de clase genera una contraseña basada en los caracteres permitidos y en la longitud dada.
    @staticmethod
    def generate_password(length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True,
                          not_allowed='', customized='') -> str:
        
        # Esta es la lista que almacena los caracteres de la contraseña.
        password = []
        
        # estos son todos los caracteres por defecto opcionales para la contraseña.
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

Después de eso, hay algunas validaciones para los parámetros, tales como que 'length' sea un entero positivo, o que 
'use_uppercase', 'use_numbers' y 'use_punctuations' sean valores booleanos.

```python
        # Esto valida que la longitue es un entero.
        if not isinstance(length, int):

            raise TypeError('The number must be a positive integer')
        
        # Esto asegura que la longitud es un entero positivo.
        if length <= 0:

            raise ValueError('The number must be a positive integer')
        
        # Esto asegura que todos los argumentos para permitir mayúsculas, números y/o puntuaciones son valores booleanos.
        if not (
                isinstance(use_uppercase, bool) and isinstance(use_numbers, bool) and isinstance(use_punctuations, bool)
        ):

            raise TypeError('use_uppercase, use_numbers and use_punctuations must be boolean')
```

Después, si el parámetro 'customized' es dado, esto valida que es una contraseña. Posterior a eso, los caracteres 
duplicados son eliminados y los caracteres restantes son añadidos en la lista 'password'.

```python
        # Si caracteres personalizados son dados:
        if customized:
            
            # Esto asegura que los caracteres personalizados son una cadena.
            if not isinstance(customized, str):

                raise TypeError('Customized characters must be a string')
            
            # Esto elimina caracteres duplicados en los caracteres personalizados.
            customized = set(customized)
            
            # Esto añade los caracteres personalizaos en la lista 'password'.
            password.extend(list(customized))
```

Estas validaciones son hechas con los caracteres de 'not_allowed' también, esto asegura que 'not_allowed' es una cadena, 
y si 'customized' es dado también, esto asegura que no hay caracteres colisionando entre ellos. Finalmente, si todos los 
caracteres en 'not_allowed' son los mismos de cualquier situación \(por ejemplo, '1234567890' tiene los mismos caracteres 
que '0123456789'), habrá un error.

```python
        # Si son dados caracteres no permitidos:
        if not_allowed:
            
            # Esto asegura que los caracteres no permitidos son una cadena.
            if not isinstance(not_allowed, str):

                raise TypeError('Not allowed characters must be a string')
            
            # Esto borra los caracteres duplicados en los caracteres no permitidos.
            not_allowed = set(not_allowed)
            
            # Esto asegura que no hay caracteres idénticos entre los caracteres personalizados y los no permitidos.
            if customized and any(letter in customized for letter in not_allowed):

                raise ValueError('A character is crashing in customized and not allowed characters')
            
            # Por cada cadena de caracteres almacenada como valores en el diccionario inicial:
            for characters_string in cls.type_of_characters.values():
                
                # Esto asegura que los caracteres no permitidos no invalidan ninguna cadena de caracteres.
                # Si todos los caracteres no permitidos son los mismos de una cadena de caracteres (mayúsculas, números, puntuaciones)
                # Por ejemplo, 0123456789 tiene los mismos caracteres de 1234567890, el orden no importa.
                if all(c in not_allowed for c in characters_string) or all(c in not_allowed for c in string.ascii_lowercase):

                    raise ValueError('Not allowed characters are the same characters of lower, upper, digits or punctuation characters, instead set its parameter as False')
```

Si se pasan todas las validaciones, entonces cada caracter de 'not_allowed' será usado para checar si el caracter está 
en cualquier situación y lo removerá. Si el caracter no está en la situación, no hace nada.

```python
            # Por cada situación (clave) y cadena de caracteres (valor) en el diccionario original:
            for situation, characters_string in cls.type_of_characters.items():
                
                # Por cada caracter de los caracteres no permitidos:
                for character in not_allowed:
                    
                    # Si el caracter está en una cadena de caracteres:
                    if character in characters_string:
                        
                        # Esto elimina el caracter de la cadena de caracteres y reemplaza la cadena en el diccionario.
                        cls.type_of_characters[situation] = cls.type_of_characters[situation].replace(character, '')
                    
                    # Si la condición de arriba no se cumple, y si el caracter está en los caracteres por defecto (minúsculas):
                    elif character in characters:

                        # Esto elimina el caracter de los caracteres por defecto y lo reemplaza.
                        characters = characters.replace(character, '')
```

Posterior a eso, el parámetro de cada situación opcional y sus respectivos caracteres \(sin los caracteres no permitidos) 
son almacenados en un diccionario como valores, y añade una letra minúscula en la contraseña.

```python
        # Esto almacena las situaciones en un diccionario como las claves, y sus valores booleanos y los caracteres 
        # relacionados como valores.
        situations = {'uppercase': (use_uppercase, type_of_characters['uppercase']),
                      'numbers': (use_numbers, type_of_characters['numbers']),
                      'punctuations': (use_punctuations, type_of_characters['punctuations']),
                      }
    
        # Esto añade un caracter cualquiera de los por defecto (o los caracteres disponibles si cualquier caracter fuera eliminado)
        password.append(secrets.choice(characters))
```

Después un ciclo for añade 1 caracter de cada uno de los tipos de caracteres si esos son 'True' en los parámetros arriba, 
esto asegura que al menos 1 de cada tipo es añadido.

```python
        # El ciclo for checa si las situaciones son True o False.
        for character_type in situations.values():
    
            if character_type[0]:
                
                # Si la situación está permitida (o su parámetro es True) añade los caracteres especificados como posibles
                # para la contraseña
                characters += character_type[1]
                
                # También añade 1 caracter de cada tipo permitido para asegurar que hay al menos 1.
                password.append(secrets.choice(character_type[1]))
```

Posterior a eso, la longitud sobrante se calcula, si 'remaining' es negativo, significa que probablemente la cadena 'customized' 
tuvo más caracteres de los posibles \(por ejemplo, la longitud de la contraseña debería ser igual a 5, pero customized='asf23842jw'), 
y entonces habrá un error. Si 'remaining' es positivo significa que la contraseña sigue necesitando caracteres, dado eso, la lista 
'random_password' almacenará los caracteres sobrantes necesarios para completar la contraseña, y finalmente, con un list 
comprehension, los caracteres necesarios son escogidos y añadidos en la lista.

```python
        # Esta es la longitud necesaria para completar la contraseña.
        remaining = length - len(password)
        
        # Si el sobrante es negativo significa que la longitud de la contraseña generada es más grande que la dada como 
        # argumento.
        if remaining < 0:

            raise ValueError('Length of custom characters is greater than characters available in password, reduce it')
        
        # Si el sobrante es positivo significa que faltan caracteres en la contraseña.
        elif remaining > 0:
            
            # Selecciona todos los caracteres necesarios para completar la contraseña.
            random_password = [secrets.choice(characters) for _ in range(remaining)]
            
            # Extiende la lista original 'password' con la lista de arriba.
            password.extend(random_password)
```

Finalmente, cuando el proceso arriba termina \(o 'remaining' es igual a 0, que significa que la contraseña está completa), 
los caracteres en la lista son revueltos aleatoriamente y unidos como una cadena.

```python
        # Si el sobrante es igual a 0 significa que la contraseña está completa.
        # La lista 'password' es revuelta para evitar patrones.
        secrets.SystemRandom().shuffle(password)
        
        # Finalmente, los caracteres revueltos son unidos en una cadena.
        final_password = ''.join(password)
        
        # Retorna la contraseña segura.
        return final_password
```

Y se retorna la contraseña. Woohoo!

### Método estático calculate_entropy():

El método calcula la entropia en bits de la contraseña, esto es útil para calcular el tiempo para descifrar la 
contraseña y también muestra cuán segura es la contraseña. El métood usa el módulo 'math' para usar el logaritmo base 2. 

El método tiene 2 parámetros:

+ password:
Esta es la contraseña creada \(o puede ser cualquier contraseña), debe ser una cadena.

+ decimals:
Este parámetro define cuántos decimales habrá en la entropía \(Y si es necesario, redondea la entropía a ese número de 
decimales). Por defecto, hay 1 decimal.

```python
    # Este método calcula la entropía de la contraseña dada.
    @staticmethod
    def calculate_entropy(password: str, decimals: int = 1) -> Union[int, float]:
```

Antes de que el método comience, validamos los parámetros, y si no hay algún error, continuamos.

```python
        # Esto asegura que la contraseña dada es una cadena
        if not isinstance(password, str):

            raise TypeError('password must be a string')
        
        # Esto asegura que el número de decimales requerido es un entero.
        if not isinstance(decimals, int):

            raise TypeError('The number of decimals must be an integer')
        
        # Esto asegura que el número de decimales requerido es mayor o igual a 0.
        if decimals < 0:

            raise ValueError('The number of decimals must be a positive integer')
```

Primero, todos los caracteres son almacenados en un conjunto para evitar caracteres repetititvos, también necesitaremos 
calcular la longitud de la contraseña. Y finalmente, inicializamos la variable 'argument_log' como 0.

```python
        # The set ensures that we don't take repetitive characters.
        unique_characters = set(password)
        
        # Calculates the length of the password.
        length_password = len(password)
        
        # Initialize the argument of the log base 2.
        argument_log = 0
```

Después, los tipos de caracteres son almacenados de nuevo en un diccionario llamado 'situations', la clave es la 
situación y los valores son los caracteres y el número de posibilidades para cada tipo.

```python
        # El diccionario almacena los posibles caracteres y el número de ellos.
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

Usamos un ciclo for para verificar si 1 \(o más, pero solo necesitamos 1 para esta verificación) caracrer de cada tipo 
está en la contraseña, y si lo está, lo añadimos al argumento el número de posibles caracteres del tipo.

```python
        # Separa los caracteres del número de posibles caracteres.
        for character_type, possibilities in situations.values():
            
            # Checa que un caracter del tipo especificado aparezca al menos una vez,
            # esto significa que el tipo de caracter está permitido en la contraseña.
            if any(character in character_type for character in unique_characters):
                
                # Si es true, suma el número de posibles caracteres al argumento del logaritmo.
                argument_log += possibilities
```

Finalmente, calculamos la entropía usando la siguiente fórmula, donde:

![Entropy formula](entropy_formula.png)

+ H: Representa la entropía de la contraseña.

+ L: Representa la longitud de la contraseña.

+ n: Representa las posibilidades totales para cada caracter en la contraseña.

```python
        # Usando la fórmula previa, calculamos su entropía y verificamos que la contraseña no esté vacía.
        entropy = length_password * math.log2(argument_log) if length_password > 0 else 0
```

Ahora, si la entropía ya es un entero, la retornamos, si no, pero el parámetro 'decimals' es igual a 0, la entropía es 
redondeada a un entero. Finalmente, si las condiciones de antes son falsas, la entropía se redondea a los decimales 
establecidos.

````python
        # Si la entropía ya es un entero:
        if isinstance(entropy, int):

            return entropy
        
        # Si la entropía no debe tener decimales, se redondea a un entero:
        if decimals == 0:

            return round(entropy)
        
        # Finalmente, retornamos la entropía redondeada a los decimales indicados.
        return round(entropy, decimals)
````

¡Y eso es todo!

### Método estático calculate_decryption_time():

La función calcula cuánto tiempo un hacker necesitaría \(teóricamente) para comprometer la contraseña, esto muestra la 
seguridad involucrada en la contraseña e indica si es una buena idea usar la contraseña.

La función tiene 3 parámetros:

+ entropy:
Esta es la entropía de la contraseña, se necesita para calcular cuántos intentos son necesarios para comprometer la
contraseña en un ataque de fuerza bruta, si la entropía es más grande, los intentos necesarios lo serán también. Debe 
ser un número positivo.

+ decimals:
Esto define cuántos decimales habrá en el tiempo para descifrar la contraseña \(en años). Por defecto, habrá 2 
decimales en el tiempo. Debe ser un entero positivo.

+ attempts_per_second:
Este es el número de intentos que un hacker puede hacer por segundo en un ataque de fuerza bruta \(obviamente, esto es 
relativo), pero lo definimos como 1*10^12 intentos por segundo por defecto. Debe ser un entero positivo.

```python
    # Este método calcula el tiempo para descifrar necesario para compromenter la contraseña \(en años) en un ataque de 
    # fuerza bruta.
    @staticmethod
    def calculate_decryption_time(entropy: Union[int, float],
                                  decimals: int = 2, 
                                  attempts_per_second: Union[int, float] = 1e12) -> Union[int, float]:
```

Antes de iniciar, validamos los parámetros, si todo es correcto, continuamos.

```python
        # Esto asegura que la entropí dada es un número.
        if not isinstance(entropy, Union[int, float]):

            raise TypeError('entropy must be a number')
        
        # Esto asegura que el número de decimales requerido es un entero.
        if not isinstance(decimals, int):

            raise TypeError('Number of decimals must be an integer')
        
        # Esto asegura que el número de decimales requeridos es más grande o igual a 0.
        if decimals < 0:

            raise ValueError('Number of decimals cannot be a negative integer')
        
        # Esto asegura que los intentos por segundo es un número.
        if not isinstance(attempts_per_second, Union[int, float]):

            raise TypeError('attempts per second must be an integer')
        
        # Esto asegura que los intentos por segundo es un entero positivo
        if attempts_per_second <= 0:

            raise ValueError('attempts per second must be a positive integer')
```

Primero, calculamos cuántos segundos son en un año.

```python
        # Segundos por año = 60 segundos * 60 minutos * 24 horas * 365 días.
        seconds_per_year = 60 * 60 * 24 * 365
```

Después de eso, calculamos cuántas combinaciones son posibles con la entropía recibida.

```python
        # Estos son todas las posibles combinaciones de la contraseña, por lo tanto,
        # todos los posibles intentos para comprometerla.
        combinations = 2 ** entropy
```

Después, calculamos el tiempo para descifrar basado en la siguiente fórmula, donde:

![Decryption_time_formula](decryption_time_formula.png)

+ T: Representa el tiempo para descifrar en años.

+ H: Representa la entropía de la contraseña.

+ V: Representa los intentos por segundo que un hacker puede hacer.

+ S: Representa los segundos en un año.

```python
        # T = 2^H / V * S
        decryption_time_in_years = combinations / (attempts_per_second * seconds_per_year)
```

Ahora, si el tiempo para descifrar ya es un entero, lo retorna, y si no lo es, pero el parámetro 'decimals' es igual a 
0, es redondeado a un entero. Finalmente, si las condiciones antes son False, es redondeadoa los decimales establecidos.

```python
        # Si el tiempo para descifrar en años es un entero:
        if isinstance(decryption_time_in_years, int):

            return decryption_time_in_years
        
        # Si la condición de arriba no se cumple, y el número de decimales dado es 0, se redondea a un entero:
        if decimals == 0:

            return round(decryption_time_in_years)
        
        # Finalmente, retornamos el tiempo redondeado a los decimales dados.
        return float(f'{decryption_time_in_years:.{decimals}e}')
```

¡Hemos terminado!

## Ejemplos

### Método de instancia create_password():

+ Uso por defecto:

En este caso, usaremos el comportamiento por defecto del método \(esto significa que todos los tipos de caracteres 
son permitidos), necesitamos una contraseña con 12 caracteres:
  
```python
#  La longitud de la contraseña es de 12 caracteres
pswrd_generator = Generator.create_password(12)
# output: UbMlRi/N5+4, 78.7, 15568.76
```

### Método estático generate_password():

Todas las siguientes contraseñas tendrán 18 caracteres.
+ Uso por defecto:

Como vimos antes, generaremos la contraseña con el comportamiento por defecto del método:
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18)
# output: +1ND%q#h2tOC-4_F$8 
```

+ Contraseña sin puntuaciones:

Ahora, la contraseña no permite caracteres de puntuación \(o, de la misma forma, solo letras minúsculas, mayúsculas y 
dígitos son permitidos):
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_punctuations=False)
# output: 6dVf1UKHUHOq0RSEUL 
```

+ Contraseña sin dígitos:

Ahora, la contraseña no permite dígitos \(o, the la misma forma, solo letras minúsculas, mayúsculas y caracteres de 
puntuación son permitidos):
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_numbers=False)
# output: vf/CE_uu!W&#Sw%jhD
```

+ Contraseña sin letras mayúsculas:

Ahora, la contraseña no permite letras mayúsculas \(o, de la misma forma, solo letras minúsculas, números y caracteres 
de puntuación son permitidos):
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_uppercase=False)
# output: /3_4!#&u991_43-m4t
```

+ Contraseña con solo letras minúsculas: 

Finalmente, la contraseña solo permite letras minúsculas:
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_uppercase=False, 
                                                 use_punctuations=False, use_numbers=False)
# output: ytvyyzlfnamurebtoh
```

+ Situaciones combinadas: 

En este caso, la contraseña permite letras minúsculas y dígitos, pero no permite letras mayúsculas y caracteres de 
puntuación:
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_uppercase=False, 
                                                 use_punctuations=False)
# output: ou0h92pj1cwqe8ny02
```

+ Contraseña con letras mayúsculas, minúsculas, dígitos y puntuaciones, además de caracteres personalizados y no permitidos: 

En este caso final, la contraseña permite todo tipo de caracteres, pero establece algunos específicos y deshabilita otros:
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(12, use_uppercase=True, use_numbers=True, use_punctuations=True,
                                                 customized='t4zA7', not_allowed='129685dfg/-'
                                                 )
# output: Qy4A&PZ3t0z7
# Como puedes ver, cada caracter de los personalizados está en la contraseña al menos una vez, y todos los caracteres en 
# los no permitidos no están en la contraseña.
```

### Método estático calculate_entropy():

Usaremos las contraseñas generadas arriba para estos ejemplos.

+ Uso por defecto:
  
Esta es la entropía de la contraseña con todos los tipos de caracteres:

```python
# Esta es la entropía de la contraseña: +1ND%q#h2tOC-4_F$8
entropy = Generator.calculate_entropy("+1ND%q#h2tOC-4_F$8")
# output: 118.0
```

+ Contraseña sin puntuaciones:

Esta es la entropía de la contraseña sin caracteres de puntuacion:

```python
# Esta es la entropía de la contraseña: 6dVf1UKHUHOq0RSEUL
entropy = Generator.calculate_entropy("6dVf1UKHUHOq0RSEUL")
# output: 107.2
```

+ Contraseña sin dígitos:

Esta es la entropía de la contraseña sin dígitos:

```python
# Esta es la entropía de la contraseña: vf/CE_uu!W&#Sw%jhD
entropy = Generator.calculate_entropy("vf/CE_uu!W&#Sw%jhD")
# output: 115.1
```

+ Contraseña sin letras mayúsculas:

Esta es la entropía de la contraseña sin letras mayúsculas:

```python
# Esta es la entropía de la contraseña: /3_4!#&u991_43-m4t
entropy = Generator.calculate_entropy("/3_4!#&u991_43-m4t")
# output: 109.6
```

+ Contraseña solo con letras minúsculas: 

Esta es la entropía de la contraseña solo con letras minúsculas:

```python
# Esta es la entropía de la contraseña: ytvyyzlfnamurebtoh
entropy = Generator.calculate_entropy("ytvyyzlfnamurebtoh")
# output: 84.6
```
  
+ Situaciones combinadas:

Finalmente, esta es la entropía de la contraseña con letras minúsculas y dígitos permitidos:

```python
# Esta es la entropía de la contraseña: ou0h92pj1cwqe8ny0
generated_password = Generator.calculate_entropy('ou0h92pj1cwqe8ny02')
# output: 93.1
```

La entropía de cada contraseña es usada para calcular su seguridad en un ataque de fuerza bruta.

### Método estático calculate_decryption_time():

Nuevamente, usaremos las contraseñas y sus entropías generadas previamente para estos ejemplos. El tiempo calculado es 
solo teórico, y es una métrica de la seguridad de la contraseña en un ataque de fuerza bruta:

+ Uso por defecto:

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña con todos los tipos de caracteres.

```python
# Este es el tiempo para descifrar la contraseña: +1ND%q#h2tOC-4_F$8
# Su entropía es 118.0
decryption_password_time = Generator.calculate_decryption_time(118.0)
# output: 1.05e+16
```

+ Contraseña sin puntuaciones:

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña sin caracteres de puntuación:

```python
# Este es el tiempo para descifrar la contraseña: 6dVf1UKHUHOq0RSEUL
# Su entropía es 107.2
decryption_password_time = Generator.calculate_decryption_time(107.2)
# output: 5910000000000.0
```

+ Contraseña sin dígitos:

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña sin dígitos:

```python
# Este es el tiempo para descifrar la contraseña: vf/CE_uu!W&#Sw%jhD
# Su entropía es 115.1
decryption_password_time = Generator.calculate_decryption_time(115.1)
# output: 1410000000000000.0
```

+ Contraseña sin letras mayúsculas:

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña sin letras mayúsculas:

```python
# Este es el tiempo para descifrar la contraseña: /3_4!#&u991_43-m4t
# Su entropía es 109.6
decryption_password_time = Generator.calculate_decryption_time(109.6)
# output: 1410000000000000.0
```

+ Contraseña con solo letras minúsculas: 

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña con solo letras minúsculas:
  
```python
# Este es el tiempo para descifrar la contraseña: ytvyyzlfnamurebtoh
# Su entropía es 84.6
decryption_password_time = Generator.calculate_decryption_time(109.6)
# output: 31200000000000.0
```
  
+ Situaciones combinadas:

Finalmente, Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña con letras mayúsculas y 
digitos permitidos:

```python
# Este es el tiempo para descifrar la contraseña: ou0h92pj1cwqe8ny02
# Su entropía es 93.1
decryption_password_time = Generator.calculate_decryption_time(93.1)
# output: 337000000.0
```

## Contribuciones

Estoy abierto y feliz de recibir cualquier contribución al proyecto. ¡Puedes hacer un pull request, reportar un bug y 
añadir nuevas funcionalidades sin ningún problema!

## Licencia

Este proyecto fue hecho bajo la licencia del MIT:
[MIT License](https://github.com/Tzintzun444/pswrd_entropy_gen/blob/main/pswrd_entropy_gen/LICENSE.txt)

## Créditos

+ Autor: Alfredo Tzintzun.

+ Librerías usadas:
    - secrets.
    - string.
    - math.
    - typing.

¡Espero que disfrutes este proyecto!