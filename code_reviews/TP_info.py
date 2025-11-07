import csv
# A.0
horarios_prog = []
codigos = []
aerolineas = []
destinos = []
horarios_part = []
terminales = []
estados = []
def leer_vuelos():
    try:
        with open('vuelos.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            primera_fila = True
            for fila in lector:
                if primera_fila:
                    primera_fila = False
                else:
                    horarios_prog.append(fila[0])
                    codigos.append(fila[1])
                    aerolineas.append(fila[2])
                    destinos.append(fila[3])
                    horarios_part.append(fila[4])
                    terminales.append(fila[5])
                    estados.append(fila[6])
        return horarios_prog, codigos, aerolineas, destinos, horarios_part, terminales, estados
    except FileNotFoundError:
        print("File not found")
        return None
leer_vuelos()

# A. 1

def donde_vas(aerolinea):
    destinos_aerolinea = []
    for i in range(len(aerolineas)):
        if aerolineas[i] == aerolinea:
            destinos_aerolinea.append(destinos[i])
    
    if not destinos_aerolinea:
        return print(f"La aerolínea {aerolinea} no existe o no vuela hoy")

    destinos_aerolinea_unicos = []
    for elem in destinos_aerolinea:
        if elem not in destinos_aerolinea_unicos:
            destinos_aerolinea_unicos.append(elem)

    mensaje = f"\n{aerolinea} vuela a {len(destinos_aerolinea_unicos)} destinos:"
    for elem in destinos_aerolinea_unicos:
        mensaje += f"\n-{elem}"
    return print(mensaje)

# A.2

def lista_unicos(lista):
    lista_u = []
    for elem in lista:
        if elem not in lista_u:
            lista_u.append(elem)
    return lista_u

def ids_despegados():
    ids_despegados = []
    for i in range(len(estados)):
        estado_solo_letras = ""
        for letra in estados[i]:
            if 65 <= ord(letra) <= 90 or 97 <= ord(letra) <= 122:
                estado_solo_letras += letra
        if estado_solo_letras == "Despegado":
            ids_despegados.append(i)
    return ids_despegados

def puntuales_x_aero(aerolinea):
    
    cant_puntuales = 0
    horarios_part_num = []
    horarios_part_num_f = []
    ids = []
    ids_f = []
    for x in range(len(estados)):
        if aerolineas[x] == aerolinea:
            horarios_part_num_e = ''
            i = 0
            while i < len(estados[x]):
                if 48 <= ord(estados[x][i]) <= 57 or estados[x][i] == ':':
                    horarios_part_num_e += estados[x][i]
                i+= 1
            horarios_part_num.append(horarios_part_num_e)
            ids.append(x)
    for y in range(len(horarios_part_num)):
        if horarios_part_num[y]:
            horarios_part_num_f.append(horarios_part_num[y])
            ids_f.append(ids[y])

    for i in range(len(horarios_part_num_f)):
        indice_global = ids_f[i]
        if horarios_prog[indice_global] == horarios_part_num_f[i]:
            cant_puntuales += 1
    
    return cant_puntuales

def vuelos_despegados_puntual():
    aerolineas_u = lista_unicos(aerolineas)
    cant_vuelos_puntuales = 0
    vuelos_puntuales = False
    for elem in aerolineas_u:
        vp_x_aero = puntuales_x_aero(elem)
        if vp_x_aero > 0:
            print(f"-{elem}: {vp_x_aero} vuelos")
            vuelos_puntuales = True
            cant_vuelos_puntuales += vp_x_aero
    if not vuelos_puntuales:
        print("Todos los vuelos han partido con demora")

    cant_despegados = len(ids_despegados())
    if cant_despegados == 0:
        print("No hay vuelos despegados")
    else: 
        promedio = round(cant_vuelos_puntuales/cant_despegados*100, 2)
        print(f"Promedio de vuelos puntuales = {promedio}%")

#vuelos_despegados_puntual()

# A.3

def destinos_compartidos():
    destinos_u = lista_unicos(destinos)
    no_dest_comp = True
    destinos_compartidos = []
    for destino in destinos_u:
        contador = 0
        aero_x_destino = []
        for i in range(len(destinos)):
            if destinos[i] == destino:
                contador += 1
                aero_x_destino.append(aerolineas[i])
        
        aero_x_destino_u = lista_unicos(aero_x_destino)
        
        if contador >= 2:
            no_dest_comp = False
            destinos_compartidos.append([destino, contador])
            mensaje = f"{destino}: {aero_x_destino_u[0]}"
            for i in range(1, len(aero_x_destino_u)):
                mensaje += f", {aero_x_destino_u[i]}"
            print(mensaje)

    destinos_comp_ord = []
    ln = len(destinos_compartidos)
    for i in range(ln):
        for j in range(ln-1-i):
            if destinos_compartidos[j][1] > destinos_compartidos[j+1][1]:
                aux = destinos_compartidos[j+1]
                destinos_compartidos[j+1] = destinos_compartidos[j]
                destinos_compartidos[j] = aux
    destinos_compartidos = destinos_compartidos[::-1]
    
    for elem in destinos_compartidos:
        destinos_comp_ord.append(elem[0])
    
    if no_dest_comp:
        print("No hay destinos compartidos")
    
destinos_compartidos()

# B.0

fechas = []
destinos = []
origen_viajeros = []
cant_viajeros = []
def leer_turistas():
    try:
        with open('turistas_por_destino.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            primera_fila = True
            for fila in lector:
                if primera_fila:
                    primera_fila = False
                else:
                    fechas.append(fila[0])
                    destinos.append(fila[1])
                    origen_viajeros.append(fila[2])
                    if fila[3]:
                        cant_viajeros.append(float(fila[3]))
                    else:
                        cant_viajeros.append(None)

        return None
    except FileNotFoundError:
        return None
leer_turistas()

# B.1
def completar_origen():
    for i in range(len(fechas)):
        #try:
            if not cant_viajeros[i]:
                if origen_viajeros[i] == 'Total':
                    if cant_viajeros[i+1] and cant_viajeros[i+2]:
                        cant_viajeros[i] = cant_viajeros[i+1] + cant_viajeros[i+2] 
                elif origen_viajeros[i] == 'Residentes':
                    if cant_viajeros[i-1] and cant_viajeros[i+1]:
                        cant_viajeros[i] = cant_viajeros[i-1] - cant_viajeros[i+1]
                elif origen_viajeros[i] == 'No residentes':
                    if cant_viajeros[i-2] and cant_viajeros[i-1]:
                        cant_viajeros[i] = cant_viajeros[i-2] - cant_viajeros[i-1]
            """if not cant_viajeros[i]:
                raise ValueError
        except ValueError:
            print(f"No se puede determinar el dato numérico para '{origen_viajeros[i]}' en el índice {i} debido a datos faltantes en los campos auxiliares.")
"""
completar_origen()


# B.2
def depurar_fechas():
    years = []
    meses = []
    dias = []
    for elem in fechas:
        years.append(elem[0:4])
        meses.append(elem[5:7])
        dias.append(elem[8:10])
    return years, meses, dias
        
def mas_visitadas():
    year = (input("Ingrese un year: "))
    years, meses, dias = depurar_fechas()
    verificado = False
    max_viajeros_por_mes = []
    while year not in years:
        year = input("Reingrese: ")
    meses_numeros = [
        '01', '02', '03', '04',
        '05', '06', '07', '08',
        '09', '10', '11', '12'
    ]
    meses_nombres = [
        'Enero', 'Febrero', 'Marzo', 'Abril',
        'Mayo', 'Junio', 'Julio', 'Agosto',
        'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    for i in range(len(meses_nombres)):
        cant_max_viajeros = -1
        max_viajeros = ""
        for x in range(len(origen_viajeros)):
            if origen_viajeros[x] == 'No residentes' and cant_viajeros[x] != None and destinos[x] != 'CABA' and year == years[x]:
                if meses[x] == meses_numeros[i] and cant_viajeros[x] > cant_max_viajeros:
                    max_viajeros = destinos[x]
                    cant_max_viajeros = cant_viajeros[x]
        if cant_max_viajeros == 0:
            max_viajeros_por_mes.append("-")
        else:
            max_viajeros_por_mes.append(max_viajeros)

    print(f"Destinos mas visitados por mes en {year}")
    for y in range(len(meses_nombres)):
        print(f"- {meses_nombres[y]}: {max_viajeros_por_mes[y]}")
        
    return max_viajeros_por_mes

#mas_visitadas()

# B.3
years = []
localidades = []
medias = []
def leer_media_turistas_residentes_sin_CABA():
    try:
        with open('tur_int_turistas_residentes_estadia_media_anual_destino_serie.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            primera_fila = True
            for fila in lector:
                if primera_fila:
                    primera_fila = False
                else:
                    if fila[1] != 'CABA':
                        years.append(fila[0])
                        localidades.append(fila[1])
                        medias.append(float(fila[2]))
        return None
    except FileNotFoundError:
        return None

def mayor_proporcion_residentes():
    leer_media_turistas_residentes_sin_CABA()
    print("Localidad con mayor prorcion media de turistas-residentes: ")
    years_unicos = lista_unicos(years)
    for year in years_unicos:
        max_localidad = ''
        media_max = 0
        for i in range(len(localidades)):
            if medias[i] > media_max and years[i] == year:
                max_localidad = localidades[i]
                media_max = medias[i]
        print(f"-{year}: {max_localidad}")

#mayor_proporcion_residentes()
