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
        (self._generated_password, self._entropy_of_password,
         self._decryption_password_time) = self.create_password()
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
            
            # Este es el mensaje de error.
            return f'There was an error: {exception}'
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
Y finalente, este es un valor booleano, true por defecto. Incluye al menos 1 character de puntuación \(.#$%/! por ejemplo) 
en la contraseña, también puede ser más de 1.

El método usa los módulos de 'string' y 'secrets' para su funcionamiento. El uso de letras minúsculas es obligatorio, y 
todos los parámetros por defecto están en el diccionario llamado 'situations' con sus respectivos caracteres como valor.
 
```python
    # Este método genera la contraseña basado en los caracteres permitidos y la longitud dada.
    @staticmethod
    def generate_password(length: int, use_uppercase=True,
                          use_numbers=True, use_punctuations=True) -> str:
        
        # Asegura que la longitud es un entero positivo.
        if length <= 0:
          
            # Mensaje de error.
            raise ValueError('The number must be a positive integer')
        
        # Selecciona el caracter en minúscula por defecto en la variable 'characters' que contiene todos los posibles
        # caracteres.
        characters = string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz

        # Almacena las situaciones como clave en un dictionario, y sus valores booleanos y sus caracteres relacionados 
        # como los valores.
        situations = {'uppercase': (use_uppercase, string.ascii_uppercase), # True, ABCDEFGHIJKLMNOPQRSTUVWXYZ
                      'numbers': (use_numbers, string.digits), # True, 0123456789
                      'punctuations': (use_punctuations, string.punctuation), # True, !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                      }
```

Después crea la lista 'password', aquí serán almacenados todos los caracteres de la contraseña. Entonces, un ciclo for 
añadirá 1 caracter de cada uno de los tipos de caracteres si son True en los parámetros de arriba, esto asegura que al 
menos 1 de cada tipo fue añadido.

```python
        # Esta es la lista que almacena los caracteres de la contraseña.
        password = []
        
        # El ciclo for checa si las situaciones son True o False.
        for character_type in situations.values():
    
            if character_type[0]:
                
                # Si la situación está permitida (o su parámetro es True) añade los caracteres especificados como posibles 
                # para la contraseña
                characters += character_type[1]
                
                # También añade 1 caracter de cada tipo permitido para asegurar que hay al menos 1.
                password.append(secrets.choice(character_type[1]))
```

Después de eso, la longitud restante es calculada y con un list comprehension, los caracteres necesarios son elegidos y 
añadidos en la lista, la cual es unida con nuestra lista 'password'.

```python
        # Esta es la longitud necesaria para completar la contraseña.
        remaining = length - len(password)
        
        # Selecciona los caracteres necesarios para completar la contraseña.
        random_password = [secrets.choice(characters) for _ in range(remaining)]
        
        # Extiende la lista original 'password' con la lista de arriba.
        password.extend(random_password)
```

Finalmente, los caracteres en la lista son revueltos aleatoriamente y se unen en una cadena.

```python
        # La lista 'password' es revuelta para evitar patrones.
        secrets.SystemRandom().shuffle(password)
        
        # Finalmente, los caracteres revueltos son unidos en una cadena.
        final_password = ''.join(password)
        
        # Retorna la contraseña segura.
        return final_password
```

Y la contraseña se retorna. Woohoo!

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

Primero, todos los caracteres son almacenados en un conjunto para evitar caracteres repetititvos, también necesitaremos 
calcular la longitud de la contraseña. Y finalmente, inicializamos la variable 'argument_log' como 0.

```python
        # El conjunto asegura que no no tomamos caracteres repetitivos.
        unique_characters = set(password)
        
        # Calcula la longitud de la contraseña
        length_password = len(password)
        
        # Inicializa el argumento del logaritmo base 2.
        argument_log = 0
```

Después, los tipos de caracteres son almacenados de nuevo en un diccionario llamado 'situations', la clave es la 
situación y los valores son los caracteres y el número de posibilidades para cada tipo.

```python
        # El diccionario almacena los posibles caracteres y el número de ellos.
        situations = {'uppercase': (string.ascii_uppercase, 26), # ABCDEFGHIJKLMNOPQRSTUVWXYZ, 26
                      'lowercase': (string.ascii_lowercase, 26), # abcdefghijklmnopqrstuvwxyz, 26
                      'numbers': (string.digits, 10), # 0123456789, 10
                      'punctuations': (string.punctuation, 32), # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~, 32
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

Y retornamos la entropía redondeada a los decimales definidos al inicio del método.

```python
        # Usando la fórmula previa, calculamos su entropía y verificamos que la contraseña no esté vacía.
        entropy = length_password * math.log2(argument_log) if length_password > 0 else 0
        
        # Finalmente, retornamos la entropia redondeada a los decimales indicados.
        return round(entropy, decimals)
```

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
                                  decimals: int = 2, attempts_per_second=1e12) -> Union[int, float]:
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

Finalmente, retornamos el tiempo redondeado a los decimales indicados al inicio del método.

```python
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
pswrd_generator = Generator.create_password(12) # La longitud de la contraseña es de 12 caracteres
# output: UbMlRi^N5)4, 78.7, 15568.76
```

### Método estático generate_password():

Todas las siguientes contraseñas tendrán 18 caracteres.

+ Uso por defecto:

Como vimos antes, generaremos la contraseña con el comportamiento por defecto del método:
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18)
# output: `1ND%q#h2tOC:4'F]8 
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

Ahora, la contraseña no permite dígitos \(o, de la misma forma, solo letras minúsculas, mayúsculas y caracteres de 
puntuación son permitidos):
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_numbers=False)
# output: vf?CE'uu;W&~Sw^jhD 
```

+ Contraseña sin letras mayúsculas:

Ahora, la contraseña no permite letras mayúsculas \(o, de la misma forma, solo letras minúsculas, números y caracteres 
de puntuación son permitidos):
  
```python
# Esta es la contraseña requerida.
generated_password = Generator.generate_password(18, use_uppercase=False)
# output: &3_4]}[u991!43+m4t
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

### Método estático calculate_entropy():

Usaremos las contraseñas generadas arriba para estos ejemplos.

+ Uso por defecto:
  
Esta es la entropía de la contraseña con todos los tipos de caracteres:

```python
# Esta es la entropía de la contraseña: `1ND%q#h2tOC:4'F]8
entropy = Generator.calculate_entropy("`1ND%q#h2tOC:4'F]8")
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
# Esta es la entropía de la contraseña: vf?CE'uu;W&~Sw^jhD
entropy = Generator.calculate_entropy("vf?CE'uu;W&~Sw^jhD")
# output: 115.1
```

+ Contraseña sin letras mayúsculas:

Esta es la entropía de la contraseña sin letras mayúsculas:

```python
# Esta es la entropía de la contraseña: &3_4]}[u991!43+m4t
entropy = Generator.calculate_entropy("&3_4]}[u991!43+m4t")
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
# Este es el tiempo para descifrar la contraseña: `1ND%q#h2tOC:4'F]8
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
# Este es el tiempo para descifrar la contraseña: vf?CE'uu;W&~Sw^jhD
# Su entropía es 115.1
decryption_password_time = Generator.calculate_decryption_time(115.1)
# output: 1410000000000000.0
```

+ Contraseña sin letras mayúsculas:

Este es el tiempo de descifrado necesario \(en años) para comprometer la contraseña sin letras mayúsculas:

```python
# Este es el tiempo para descifrar la contraseña: &3_4]}[u991!43+m4t
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