La frase interminable

**Objetivo:** El objetivo de este ejercicio es simular el juego "La frase interminable", en el que una serie de jugadores deben ir formando una historia agregando una palabra cada vez, pero deben repetir todas las palabras previamente dichas, lo que hace que la frase se vuelva cada vez más larga y difícil de recordar.

**Enunciado:**

1. **Entrada de Jugadores:**   
   * El programa debe generar el número de jugadores, entre 2 y 4\.

2. **Reglas del Juego:**  
   * El primer jugador inicia con una palabra.  
   * El siguiente jugador repite la frase que ha formado hasta el momento y agrega una nueva palabra.  
   * Este proceso se repite hasta que todos los jugadores hayan participado y vuelve a iniciar desde el primer jugador.  
   * Cada jugador debe recordar y repetir todas las palabras de la frase en el orden en que fueron agregadas, y añadir una nueva palabra al final de la frase.  
   * Si un jugador no recuerda correctamente las palabras previas o se equivoca al agregar su palabra, el juego termina y se declara un error.  
   * El programa debe verificar que las palabras ingresadas por cada jugador sean correctas (es decir, que la secuencia de palabras siga siendo la misma que la formada hasta ese momento).

3. **Interacción con el Usuario:**  
   * Los jugadores deben ingresar en cada turno toda la frase formada hasta el momento, seguido de una única palabra adicional.  
   * Luego de cada ingreso del usuario, el programa debe mostrar la secuencia completa de palabras que se ha formado hasta ese momento.

   * En caso de error (si un jugador no recuerda la frase correctamente), el juego termina y se muestra un mensaje indicando el error.  
       
4. **Reglas de palabras válidas**

   * De haber más de un espacio entre las palabras ingresadas, el programa debe ignorarlos, de modo que el jugador no pierda como consecuencia de ingresar palabras separadas por más de un espacio.  
   * El programa no debe distinguir entre mayúsculas y minúsculas. Siempre deberá mostrar toda la frase formada en letras minúsculas.

   * El programa no debe aceptar palabras que tengan caracteres no alfabéticos como números o símbolos, en caso que esto suceda se deberá volver a ingresar la palabra hasta que sea válida.  
5. **Salida:**

   * Al final de cada turno, se debe mostrar la frase completa hasta ese momento.  
   * En caso de error, se debe mostrar el mensaje "¡Error\! El jugador X olvidó o erró la frase", donde "X" es el número del jugador que cometió el error.

6. **Ejemplo de flujo de juego:**

   Número de jugadores: 13

   Ingrese 2-4 jugadores

   Número de jugadores: 3

   Jugador 1: "El"

   Jugador 2: "el perro"

   Jugador 3: "el perro corre"

   Jugador 1: "El perro    corre muy"

   Jugador 2: “El perro corre muy deprisa ”

   Jugador 3: “El perro va muy deprisa”

   ¡Error\! El jugador 3 olvidó o erró la frase.

