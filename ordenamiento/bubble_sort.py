def ordenamiento_asc(lista):
    longitud_lista = len(lista)
    for i in range(longitud_lista):
        # El "-i" esta porque como estamos ordenando los ultimos elementos primero
        # entonces cuanto mas crece i, menos elementos tenemos que chequear
        # El "-1" esta porque estamos comparando con el siguiente (Ver visualizacion)
        # pensar que si llegamos al ultimo literal y queremos comparar con el siguiente,
        # nos vamos a exceder del limite
        for j in range(longitud_lista - i - 1):
            if lista[j] > lista[j + 1]:
                # Si el actual, es mayor al siguiente, swapeamos
                aux = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = aux
    return lista

