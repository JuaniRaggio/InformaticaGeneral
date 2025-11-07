#set document(
  title: "Review TP info general",
  author: "Juan Ignacio Raggio",
)

#set page(
  paper: "a4",
  margin: (
    top: 2.5cm,
    bottom: 2.5cm,
    left: 2cm,
    right: 2cm,
  ),
  numbering: "1",
  number-align: bottom + right,

  header: [
    #set text(size: 9pt, fill: gray)
    #grid(
      columns: (1fr, 1fr, 1fr),
      align: (left, center, right),
      [Juan Ignacio Raggio],
      [Matias Ivulich],
      [#datetime.today().display("[day]/[month]/[year]")]
    )
    #line(length: 100%, stroke: 0.5pt + gray)
  ],

  footer: context [
    #set text(size: 9pt, fill: gray)
    #line(length: 100%, stroke: 0.5pt + gray)
    #v(0.2em)
    #align(center)[
      Pagina #counter(page).display() de #counter(page).final().first()
    ]
  ]
)

#set text(
  font: "JetBrains Mono",
  size: 11pt,
  lang: "es",
  hyphenate: true,
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 0em,
  spacing: 1.2em,
)

#set heading(numbering: "1.1")
#show heading.where(level: 1): set text(size: 16pt, weight: "bold")
#show heading.where(level: 2): set text(size: 14pt, weight: "bold")
#show heading.where(level: 3): set text(size: 12pt, weight: "bold")

#show heading: it => {
  v(0.5em)
  it
  v(0.3em)
}

#set list(indent: 1em, marker: ("•", "◦", "▪"))
#set enum(indent: 1em, numbering: "1.a.")

#show raw.where(block: false): box.with(
  fill: luma(240),
  inset: (x: 3pt, y: 0pt),
  outset: (y: 3pt),
  radius: 2pt,
)

#show raw.where(block: true): block.with(
  fill: luma(240),
  inset: 10pt,
  radius: 4pt,
  width: 100%,
)

#show link: underline

// ====================================
// FUNCIONES UTILES
// ====================================

// Funcion para crear una caja de nota/observacion
#let nota(contenido) = {
  block(
    fill: rgb("#E3F2FD"),
    stroke: rgb("#1976D2") + 1pt,
    inset: 10pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(weight: "bold", fill: rgb("#1976D2"))[Nota:] #contenido
  ]
}

// Funcion para crear una caja de advertencia
#let importante(contenido) = {
  block(
    fill: rgb("#FFF3E0"),
    stroke: rgb("#F57C00") + 1pt,
    inset: 10pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(weight: "bold", fill: rgb("#F57C00"))[Importante:] #contenido
  ]
}

// Funcion para crear una caja de error comun
#let error(contenido) = {
  block(
    fill: rgb("#FFEBEE"),
    stroke: rgb("#D32F2F") + 1pt,
    inset: 10pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(weight: "bold", fill: rgb("#D32F2F"))[Error Comun:] #contenido
  ]
}

// Funcion para crear una caja de tip
#let tip(contenido) = {
  block(
    fill: rgb("#E8F5E9"),
    stroke: rgb("#388E3C") + 1pt,
    inset: 10pt,
    radius: 4pt,
    width: 100%,
  )[
    #text(weight: "bold", fill: rgb("#388E3C"))[Tip:] #contenido
  ]
}

// ====================================
// PORTADA
// ====================================

#align(center)[
  #v(1em)
  #text(size: 24pt, weight: "bold")[Informatica General]
  #v(0.5em)
  #text(size: 18pt)[Tips y Errores Trabajo practico]
  #v(0.5em)
  #text(size: 12pt, fill: gray)[
    Alumno: Matias Ivulich\
    #datetime.today().display("[day]/[month]/[year]")
  ]
  #v(1em)
]

#line(length: 100%, stroke: 1pt)
#v(1em)

= Resumen General

#importante[
  1. Si bien las funciones implementadas cumplen con los requisitos del enunciado, el codigo tiene problemas de mantenibilidad y estructura
  2. No voy a mencionar todas las veces que se repite cada error, la idea es que se entiendan los conceptos y los apliques en todos lados
  3. Quiero que le des enfasis a entender los conceptos para aplicarlos en otros contextos mas que las correcciones especificas
]

= Problemas importantes

== Uso Excesivo de Variables Globales

#error[
  Se usan multiples listas globales (horarios_prog, codigos, aerolineas, destinos, etc.) que dificultan el seguimiento del codigo y pueden causar errores dificiles de encontrar
]

El uso de variables globales no solo es una mala practica sino que
- Hace que las funciones dependan de estado externo (no deberia ser asi)
- Puede causar efectos secundarios inesperados

#tip[
  Minimiza el uso de variables globales (en lo posible eliminalo), es muchisimo mejor pedir las variables por parametro en las funciones y trabajar con esos datos
]

```python
# Codigo actual (lineas 3-9)
horarios_prog = []
codigos = []
aerolineas = []
destinos = []
horarios_part = []
terminales = []
estados = []
```

#importante[
  En el enunciado se menciona que:
_La función de lectura debe leer un archivo CSV cuyo parámetro de entrada es la ruta
del archivo ("vuelos.csv") y devolver siete listas que representan los distintos campos
de datos leídos_

  Por lo tanto, ahi ya nos estan diciendo que la funcion debe:
  - *devolver $=$ retornar: siete listas*
  - *parametro de entrada -> ruta al csv*
  Entonces es incorrecto crear las listas como variables globales y faltaria el *parametro de entrada*, el approach correcto seria:

```py
# Antes la ruta estaba "hardcodeada" == escribir la ruta a mano
# pensa que si le cambias el nombre al archivo se te rompe todo el codigo
# por lo que es mucho mejor recibirlo como parametro asi tu funcion
# puede ser reutilizable
def leer_vuelos(ruta_a_archivo): # IMPORTANTE el parametro y no hardcodearlo
    try:
        with open(ruta_a_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            primera_fila = True
            horarios_prog = []
            codigos = []
            aerolineas = []
            destinos = []
            horarios_part = []
            terminales = []
            estados = []
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
        # Retornamos como nos pedian las 7 listas
        return horarios_prog, codigos, aerolineas, destinos, horarios_part, terminales, estados
    except FileNotFoundError:
        print(f"File not found: {ruta_a_archivo}")
        return [] # preferible retornar lista vacia que none
```
]

#pagebreak()

#nota[
  - En la seccion B se vuelve a cometer este error en `leer_media_turistas_residentes_sin_CABA`
]

#importante[ MUY IMPORTANTE.

  1. Notar que la mayoria de tus funciones no reciben parametros y optas por
    usar las instancias globales y es un problema grave ese *evitalo a toda
    costa porque te van a bajar muchos puntos por eso*
  2. Aprovecha la mutabilidad de las listas en vez de variables globales.
    Que quiere decir esto? *Cuando pasas una lista por parametro y la 
    modificas, se ve reflejado el cambio en la misma* (a diferencia de los
    "built-in" como los int, strings, float). 
    ```py
    def funcion_modificadora(lista):
        lista.append(69)
        lista.append(420)

    # Luego el usuario hace:
    mi_lista = []
    funcion_modificadora(mi_lista)
    print(mi_lista) # -> [69, 420] -> Se modifico la lista del usuario
    ```

  3. Aunque los parametros no sean listas, aprovecha los valores de retorno 
    y que en todo caso el usuario haga:
    ```py
    def funcion_retornadora(arg1, arg2):
        arg1 = arg1 + arg2 # ESTO NO MODIFICA arg1
        variable_local = arg1 * arg2
        # procesamiento de datos
        return variable_local

    arg1 = 3
    arg2 = 4
    # Si el usuario quiere modificar arg1, que lo haga el, no corresponde
    # que desde la funcion hagas acceso a variables globales
    arg1 = funcion_retornadora(arg1, arg2)
    ```

  3. *Lee muy bien* que es lo que te pide el enunciado, si te dicen que una
    _funcion tiene que retornar ciertas cosas_ y _recibir por parametro 
    ciertas otras_, asegurate de cumplirlo.
  Como extra: _Te va a resultar mucho mas facil seguir tus funciones si en
  vez de usar variables globales, usas parametros o variables locales + 
  retorno correcto, solo tenes que preocuparte de lo que esta dentro de cada
  una_
]

== Conflicto de Nombres de Variables

#error[
  La variable `destinos` se define dos veces: una vez en la linea 6 para los vuelos y otra vez en la linea 167 para los turistas. Esto sobrescribe los datos de vuelos.
  _Este problema se arrastra por haber usado variables globales en vez de 
  parametros/variables locales_
]

```python
# Linea 6
destinos = []  # Para vuelos

# Linea 167 (redefinicion!)
destinos = []  # Para turistas
```

Esto causa que despues de ejecutar `leer_turistas()`, la variable global `destinos` ya no contiene los destinos de vuelos sino los de turistas, rompiendo todas las funciones anteriores.

#tip[
  Usar nombres mas descriptivos como `destinos_vuelos` y `destinos_turistas`.
  Mejor aun *no usar variables globales*
]

== Funciones que Retornan print()

#error[
  La funcion `donde_vas()` retorna el resultado de `print()`, que siempre es `None`. Esto es incorrecto, con llamar a print, ya escribis en pantalla
]

```python
# Lineas 40 y 50
def donde_vas(aerolinea):
    # ...
    if not destinos_aerolinea:
        # Estas retornando None
        return print(f"La aerolínea {aerolinea} no existe...")
    # ...
    # Estas retornando None
    return print(mensaje)
```

#importante[
  Notemos denuevo que en el enunciado nos dicen:
  - muestre por pantalla los distintos destinos a los que vuela una aerolinea
  - *devolver = retornar: la cantidad de destinos unicos* (estas devolviendo None actualmente)
  Por lo tanto aunque escribas en pantalla los destinos correctos, estas retornando None y no es lo que te piden. Este error pueden tomarlo como conceptual y podrian restarte bastantes puntos, tene cuidado con eso.
  *print (en python) retorna siempre None*
]

== Acceso a Indices Sin Validacion

#error[
  En `completar_origen()` (lineas 193-211), se accede a indices como `i+1`, `i+2`, `i-1`, `i-2` sin verificar que esten dentro de los limites de la lista. Esto puede causar IndexError.
]

```python
# Lineas 196-205
if not cant_viajeros[i]:
    if origen_viajeros[i] == 'Total':
        if cant_viajeros[i+1] and cant_viajeros[i+2]:  # Puede fallar
            cant_viajeros[i] = cant_viajeros[i+1] + cant_viajeros[i+2]
```

#tip[
  Validar los indices antes de usarlos:

  ```python
  if not cant_viajeros[i]:
      if origen_viajeros[i] == 'Total':
          if i+2 < len(cant_viajeros) and cant_viajeros[i+1] and cant_viajeros[i+2]:
              cant_viajeros[i] = cant_viajeros[i+1] + cant_viajeros[i+2]
  ```

  Mejor aun, recorrer los datos en grupos de 3 (Total, Residentes, No residentes).
]

== Calculo de Puntualidad

La lista `horarios_part` se carga al principio desde el CSV pero luego no se usa, lo que indica un error conceptual. La puntualidad debe verificarse comparando el horario programado con el horario de partida real.
No termine de entender lo que hiciste pero te dejo el razonamiento general del problema

#tip[
  La lógica correcta sería:
  1. Recorrer todos los vuelos.
  2. Verificar si el estado del vuelo es "Despegado".
  3. Si despegó, comparar `horarios_prog[i]` con `horarios_part[i]`. Si son iguales, el vuelo fue puntual.

  No es necesario (y es incorrecto) extraer la hora del string de estado.
]

= Problemas de Estructura y Diseño

== Mezcla de Logica con inputs de usuario

#importante[
  La funcion `mas_visitadas()` (lineas 225-253) mezcla la logica de procesamiento con la interaccion con el usuario (input). Esto hace que la funcion sea imposible de testear automaticamente (sin que haya alguien escribiendo a mano los inputs).
  Tene en cuenta que la idea de las funciones es que no dependan de nada externo y asi poder testearlas de forma aisladas a cualquier otra cosa, va de la mano con el problema del uso de variables globales
]

```python
# Linea 226
def mas_visitadas():
    year = (input("Ingrese un year: ")) # No va el input dentro de la funcion de procesamiento
    # ... mas logica ...
    while year not in years:
        year = input("Reingrese: ")
```

#importante[
  Separar la logica de la interfaz:

  ```python
  def calcular_mas_visitadas(year, years_data, meses_data, ...):
      """Calcula los destinos mas visitados por mes para un año dado"""
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
      if year not in years_data:
          raise ValueError(f"Año {year} no encontrado en los datos")
      # ... logica de procesamiento ...
      return max_viajeros_por_mes

  def mas_visitadas():
      """Presenta los datos y llama a la funcion que hace los calculos"""
      years, meses, _ = depurar_fechas()
      year = (input("Ingrese año: "))
      while year not in years:
          year = input("Reingrese: ")

      max_viajeros_por_mes = calcular_mas_visitadas(year, years, meses)

      print(f"Destinos mas visitados por mes en {year}")
      for y in range(len(meses_nombres)):
          print(f"- {meses_nombres[y]}: {max_viajeros_por_mes[y]}")
      return max_viajeros_por_mes
  ```
  Nota que `mas_visitadas()` se encarga de pedirle datos al usuario y 
  mostrar en pantalla la informacion. No esta procesando la informacion,
  por otro lado, `calcular_mas_visitadas(...)` es la que se encarga del
  procesamiento de datos. Este es un concepto fundamental de la informatica,
  separar la interaccion con el usuario del procesamiento de datos.
]

#tip[
  Para ordenar todo esto, podes implementar esta "mecanizacion":
  1. Hacer la funcion de procesamiento de datos *recibiendo todo lo necesario por parametros* (obviamente creas variables locales si es necesario)
  2. Hacer la *funcion de presentacion* que va a *llamar* a la *funcion de procesamiento de datos*

  Entonces la funcion que te pidieron que *recibe input por teclaro* es la de presentacion que internamente llama a la de procesamiento.

  Mas tecnicamente el Frontend es la funcion de recibir input y el Backend la funcion de procesamiento de datos
]

#pagebreak()

= Legibilidad y Estilo

== Nombres de Variables Poco Descriptivos

#importante[
  En algunas funciones, como `puntuales_x_aero`, se usan nombres de variables muy cortos y poco descriptivos (ej. `horarios_part_num_e`, `horarios_part_num_f`, `ids`, `ids_f`). Esto hace que el codigo sea dificil de seguir. Intenta usar nombres que describan claramente que guarda la variable.

  Por ejemplo, en vez de `ids_f`, podrías usar `indices_vuelos_aerolinea`. Es mas largo, pero mucho mas claro.
]

== Magic numbers

#error[
  En `ids_despegados`, usas `65 <= ord(letra) <= 90`. Estos números se conocen como magic numbers y son una mala practica porque no se entiende a simple vista que representan.

  ```python
  if 65 <= ord(letra) <= 90 or 97 <= ord(letra) <= 122:
      estado_solo_letras += letra

  ```
]

#tip[
Te conviene hacer esto:
```py
  if 'A' <= letra <= 'Z' or 'a' <= letra <= 'z':
  estado_solo_letras += letra
```
]
#pagebreak()

= Aspectos Positivos

A pesar de los problemas mencionados, hay varios aspectos positivos en el codigo:

- El codigo funciona y cumple con los requisitos del enunciado
- Se utiliza correctamente el modulo `csv` para leer archivos
- Se implementan correctamente loops y condicionales
- Se reutiliza codigo con la funcion `lista_unicos()`
- Se utiliza encoding UTF-8 al abrir archivos
- Se manejan casos especiales (valores None, listas vacias, etc.)

= Recomendaciones Finales

1. *Eliminar variables globales*: Las funciones tienen que recibir datos como parametros y retornen resultados

2. *Separar logica de presentacion*: Hacer funciones de presentacion por separado de las funciones de procesamiento

3. *Validar datos*: Verificar indices mas que nada es practica y si necesitas hacelo en papel para tenerlo mas claro

4. *Cumplir con lo pedido en el enunciado*: Este punto es fundamental, si te dicen que una funcion recibe `dato_X` y retorna `tipo_T`, asegurate de cumplirlo. Acordarse que *print retorna None siempre*

5. *Cualquier duda que tengas escribime*

#importante[
  El trabajo demuestra comprension de los conceptos basicos, adaptar las sugerencias dadas va hacer que el codigo sea mas legible y por ende mas facil de seguir. Esto es una ventaja no solo para el dia de mañana que alguien tenga que leer tu codigo sino que para que vos mismo cuando tengas que leerlo (incluso el dia del examen), se te haga mas facil de corregir
]

