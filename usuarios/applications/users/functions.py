# funciones extra de la aplicacion users

import random
import string

# retorna un codigo de 6 digitos con numeros y letras
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))