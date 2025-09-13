numero_A = 65
print(numero_A) # escribe "41" en consola

letra_A = 'A'
print(letra_A) # escribe "A" en consola


# la computadora lo pasa a interpretar como letra -> escribe la letra
print(chr(numero_A)) 

print(ord(letra_A))

numero_65 = int("65") # -> Es el entero 65
string_65 = "65" # == str(65)

# ===========================================================================

# Lo que ingresa el usuario es siempre un string, el pasaje lo tenemos que
# hacer nosotros
numero = input("Ingrese un numero: ")

if numero == "10":
    print("numero es 10")

# ===========================================================================

# Dato Bool

# True -> 1 o valor distinto del neutro
# False -> 0 o valor neutro (en strings seria el vacio)

valido = False # o True

if valido:
    print("Valido es True")


# input siempre retorna string
# => type(input("...")) == String
cadena = input("Ingrese una cadena: ")

if cadena: # Es exactamente lo mismo que hacer bool(cadena) == True
    print("La cadena no es vacia")
else:
    print("El usuario ingreso la cadena vacia")


# Si el usuario me ingresa letras, me tira error
# Si no hago el pasaje a entero y me pasan un 0, se valua en el if como si 
# fuese una cadena
numero = int(numero)

if numero:
    print("El numero es distinto de 0")


# ===========================================================================

# type() es una funcion que retorna el tipo de dato de lo que este dentro
# (como parametro)
print(type(cadena)) # String
print(type(numero)) # Como hicimos la conversion, me va a devolver Integer

# ===========================================================================

