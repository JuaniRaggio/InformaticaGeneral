numero_limite = int(input("Ingrese el numero limite superior"))
i = int(input("Ingrese el numero limite inferior"))

while i < numero_limite:

    # Quiero ver si i es primo para encontrar el menor dentro del limite
    contador_divisores = 2
    divisor = 2
    while divisor < i:
        if i % divisor == 0:
            contador_divisores += 1
        # divisor += 1
    
    if contador_divisores == 2 and i != 1:
        primo_found = True

    # i += 1
