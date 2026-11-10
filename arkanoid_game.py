"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    texto = self.level_path.read_text()
    lineas = texto.splitlines()
    
    self.layout = []
    for linea in lineas:
        if linea != "":
            self.layout.append(linea)
            
    ancho = len(self.layout[0])
    for fila in self.layout:
        if len(fila) != ancho:
            raise ValueError("Las filas tienen distinto tamaño.")
            
    return self.layout

@arkanoid_method
def preparar_entidades(self) -> None:
    self.paddle = self.crear_rect(0, 0, self.PADDLE_SIZE[0], self.PADDLE_SIZE[1])
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET)
    
    self.score = 0
    self.lives = 3
    self.end_message = ""
    
    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    self.blocks = []
    self.block_colors = []
    self.block_symbols = []
    
    fila_idx = 0
    for fila in self.layout:
        col_idx = 0
        for simbolo in fila:
            if simbolo == "#" or simbolo == "@" or simbolo == "%":
                rect = self.calcular_posicion_bloque(fila_idx, col_idx)
                self.blocks.append(rect)
                self.block_colors.append(self.BLOCK_COLORS[simbolo])
                self.block_symbols.append(simbolo)
            col_idx += 1
        fila_idx += 1

@arkanoid_method
def procesar_input(self) -> None:
    teclas = self.obtener_estado_teclas()
    velocidad = int(self.PADDLE_SPEED)
    
    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        self.paddle.x -= velocidad
    if teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        self.paddle.x += velocidad
        
    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH

@arkanoid_method
def actualizar_bola(self) -> None:
    if self.running == False:
        return

    self.ball_pos.x += self.ball_velocity.x
    self.ball_pos.y += self.ball_velocity.y
    ball_rect = self.obtener_rect_bola()

    if ball_rect.left <= 0 or ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x *= -1
    if ball_rect.top <= 0:
        self.ball_velocity.y *= -1
        
    if ball_rect.bottom >= self.SCREEN_HEIGHT:
        self.lives -= 1
        if self.lives > 0:
            self.reiniciar_bola()
        else:
            self.running = False
            self.end_message = "¡Derrota!"
        return

    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        self.ball_velocity.y *= -1

    indice = ball_rect.collidelist(self.blocks)
    if indice != -1:
        self.ball_velocity.y *= -1
        
        simbolo = self.block_symbols[indice]
        self.score += self.BLOCK_POINTS[simbolo]
        
        self.blocks.pop(indice)
        self.block_colors.pop(indice)
        self.block_symbols.pop(indice)
        
        if len(self.blocks) == 0:
            self.running = False
            self.end_message = "¡Victoria!"

@arkanoid_method
def dibujar_escena(self) -> None:
    self.screen.fill(self.BACKGROUND_COLOR)
    
    for i in range(len(self.blocks)):
        self.dibujar_rectangulo(self.blocks[i], self.block_colors[i])
        
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    self.dibujar_circulo((int(self.ball_pos.x), int(self.ball_pos.y)), self.BALL_RADIUS, self.BALL_COLOR)
    
    self.dibujar_texto(f"Puntuación: {self.score}", (20, 20))
    self.dibujar_texto(f"Vidas: {self.lives}", (self.SCREEN_WIDTH - 120, 20))
    
    if self.end_message != "":
        self.dibujar_texto(self.end_message, (self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2), grande=True)

@arkanoid_method
def run(self) -> None:
    self.inicializar_pygame()
    self.cargar_nivel()
    self.preparar_entidades()
    self.crear_bloques()
    
    self.running = True
    
    while True:
        for evento in self.iterar_eventos():
            if evento.type == self.EVENT_QUIT:
                self.finalizar_pygame()
                return
            if evento.type == self.EVENT_KEYDOWN:
                if evento.key == self.KEY_ESCAPE:
                    self.finalizar_pygame()
                    return
                    
        if self.running == True:
            self.procesar_input()
            self.actualizar_bola()
            
        self.dibujar_escena()
        self.actualizar_pantalla()
        self.clock.tick(self.FPS)


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
