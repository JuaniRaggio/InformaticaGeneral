# 1. Fijarse en el enunciado si piden validar
# 2. Si esta ambiguo, fijate en los ejemplos

# Si hay un ejemplo asi: 44a356876 y tira error, validar

# str1 -> Si la primera letra de str1 es != str2
# str2

# "hola"
# "holaa" -> Es mayor a "hola" porque es mas largo
# "2str"

dni = input("Ingrese su dni: ")

# ===== VALIDACION ===== #

# 1. Recorrer caracter por caracter
# 2. Preguntar si son numeros
# 3. Si no son numeros -> No lo puedo pasar

pasaje_valido_a_int = True
i = 0

while i < len(dni) and pasaje_valido_a_int:
    if not ("0" <= dni[i] <= "9"):
        pasaje_valido_a_int = False
    i += 1

# A partir de aca quiero que dni sea int porque se que puedo hacer el pasaje

if pasaje_valido_a_int:
    dni = int(dni)
    if dni > 1:
        print("El dni es mayor a 1")
else:
    print("El dni fue invalido, termina el programa.")

# ===========================================================================

# Pasaje a int de un input
# 1. Fijarse si se puede pasar
# 2. Usar la funcion int


# int(variable) -----> No modifica tu variable, sino que te retorna la variable transformada


