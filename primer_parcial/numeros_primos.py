import math
# Validaciones
# ...

# Para ver si un numero es primo:
# Un numero es primo si divisible por si mismo y por uno ====> Tiene 2 divisores

# Que necesitamos?

numero = int(input("Ingrese numero"))
i = 2 # "iterador" => Por los numeros que vamos a dividir
# Aumento contador de divisores cuando <====> n % i
contador_divisores = 2
es_primo = True

while i < numero:
    if numero % i == 0:
        # Como llegamos hasta numero - 1 (i < numero) y empzamos el i en 2,
        # sabemos que si ya encontre un nuevo divisor, no es primo el numero
        # contador_divisores += 1
        es_primo = False
    i += 1

# ==============================================================================

arr = "ojsdnjkjsaskdjns"
var = arr[-1]

limite_inferior = int(input("Ingrese el limite inferior"))
limite_superior = int(input("Ingrese el limite superior"))

# { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 } <==> (li = 1, ls = 10)

# i empezaria en 22 (si voy del menor al mayor)
# { 22, 23, 24, 25, 26, 27 }

# Primo mas chico

i = limite_inferior
primo_found = False

while i <= limite_superior and not primo_found:
    # Aca tenemos el primer numero del intervalo, que quiero hacer con este numero?
    # Quiero ver si i es primo

    # Si tiene dos divisores, primo_found = True
    divisor = 2
    contador_divisores = 2
    # Contar divisores
    while divisor < i:
        if i % divisor == 0:
            contador_divisores += 1
        divisor += 1

    if contador_divisores == 2 and i != 1:
        # Si encontramos el primo, no aumentamos el iterador
        primo_found = True
        print(f"El menor numero primo es {i}")
    else:
        # Si no era primo i, voy al siguiente
        i += 1

# Aca abajo i tiene el valor del primo mas chico
# Tambien primo_found tiene la informacion de si se encontro un primo o no
# primo_found == False ===> No hubo primo (Salio por llegar al limite sup)
# Entonces tiene sentido no hacer el otro recorrido

i = limite_superior
primo_found = False

while i >= limite_inferior and not primo_found:
    # Contamos divisores
    contador_divisores = 2
    divisor = 2
    while divisor < i:
        if i % divisor == 0:
            contador_divisores += 1
            # primo_found = False ==> En realidad ya es False
        divisor += 1

    if contador_divisores == 2 and i != 1:
        primo_found = True
        print(f"El mayor numero primo es {i}")
    else:
        i -= 1

# Si no hubo primos =====> primo_found == False

# while i < 10:

#     i += 1
















i = limite_inferior

i -= 1











