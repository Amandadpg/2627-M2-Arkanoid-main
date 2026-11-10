# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

**Nivel válido y nivel inexistente**
- Se ha ejecutado el juego con niveles/demo.txt como pone en el readme, arrancando correctamente. Posteriormente, se ha probado con una ruta falsa (inventado.txt). El programa captura el error y lanza la excepción FileNotFoundError.

**Nivel con filas de distinta longitud**
- Se ha modificado temporalmente el fichero demo.txt quitando un carácter de la primera fila y se ha ejecutado. El programa detecta la asimetría geométrica y lanza correctamente el `ValueError` indicando que las filas tienen distinta longitud.

**Paleta en ambos límites de la pantalla**
- Se ha mantenido pulsada la tecla de dirección izquierda (y luego derecha) de forma continua. Las validaciones de coordenadas en procesar_input funcionan; la paleta frena al alcanzar las coordenadas 0 y el SCREEN_WIDTH.

**Rebote contra pared, paleta y cada tipo de bloque**
- Se ha jugado una partida normal observando el sistema de vectores. La bola invierte sus ejes correctamente al impactar con los bordes. La puntuación se suma según el diccionario de valores (`#`, `@`, `%`).

**Pérdida de una vida y reinicio de la bola**
- Se ha dejado caer el proyectil por el borde inferior. El contador de vidas resta 1 y se invoca a reiniciar_bola, reposicionando la bola en el centro de la paleta.

**Victoria al eliminar el último bloque y derrota al agotar vidas**
- Se ha creado un nivel de prueba (facil.txt) de un solo bloque para verificar la victoria, y se han dejado perder 3 vidas intencionadamente para la derrota. Al vaciarse la lista self.blocks aparece "¡Victoria!". Al llegar las vidas a 0, aparece "¡Derrota!". En ambos casos, el bucle de actualización se detiene.

**Salida limpia con Escape y al cerrar la ventana**
- Se ha pulsado la tecla ESCAPE y el botón de cerrar ventana durante la ejecución. El bucle de eventos detecta, ejecutando finalizar_pygame y terminando el proceso en la terminal sin errores ni procesos colgados.

Una mejora opcional no debe romper ninguno de estos casos.
