import os
import time
import cv2
import numpy as np
import random
import heapq
from collections import deque

# Configuración del juego
GRID_SIZE = 13
CELL_SIZE = 40
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (0, 165, 255)
GREY = (128, 128, 128)
BROWN = (42, 42, 165)
YELLOW = (0, 255, 255)
PURPLE = (255, 0, 255)
CYAN = (255, 255, 0)

# Tipos de power-ups
BOMB_UP = 5
FIRE_UP = 6
KICK_UP = 7
SPIKE_BOMB = 8

# Frame actual
fps = 0

textures = {
    "irrompible": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/irrompible.png"), (CELL_SIZE, CELL_SIZE)),
    "destructible": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/destructible.png"), (CELL_SIZE, CELL_SIZE)),
    "suelo": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/suelo.png"), (CELL_SIZE, CELL_SIZE)),
    "bomba": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/bomb.png"), (CELL_SIZE, CELL_SIZE)),
    "sbomb": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/sbomb.png"), (CELL_SIZE, CELL_SIZE)),
    "explosion": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/explosion.png"), (CELL_SIZE, CELL_SIZE)),
    "explosion_blue": cv2.resize(cv2.imread("../VSCode/imagenes/bomberman/explosionB.png"), (CELL_SIZE, CELL_SIZE))
}
# Cargamos en texturas las imagenes up down left right de los 4 posibles jugadores
for player_number in range (1, 4):
    for direction in ["up", "down", "left", "right"]:
        textures[f"{player_number}_{direction}"] = cv2.resize(cv2.imread(f"../VSCode/imagenes/bomberman/{player_number}_{direction}.png"), (CELL_SIZE, CELL_SIZE))


def create_default_grid():
    """
    Crear el mapa por defecto basado en la estructura clásica de Bomberman.
    """

    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 3, 3, 0, 3, 0, 3, 3, 0, 0, 1],
        [1, 0, 1, 3, 1, 3, 1, 3, 1, 3, 1, 0, 1],
        [1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1],
        [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1],
        [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
        [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1],
        [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
        [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1],
        [1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1],
        [1, 0, 1, 3, 1, 3, 1, 3, 1, 3, 1, 0, 1],
        [1, 0, 0, 3, 3, 0, 3, 0, 3, 3, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    return np.array(grid)

def create_grid():
    """
    Crear un mapa aleatorio con muros indestructibles y bloques destructibles.
    """
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    # Añadir muros indestructibles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i % 2 == 0 and j % 2 == 0:
                grid[i][j] = 1

    # Añadir bloques destructibles
    for _ in range(GRID_SIZE * GRID_SIZE // 3):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[y][x] == 0 and (x, y) not in [(1, 1), (1, 2), (2, 1), (GRID_SIZE-2, GRID_SIZE-2), (GRID_SIZE-2, GRID_SIZE-3), (GRID_SIZE-3, GRID_SIZE-2)]:
            grid[y][x] = 3  # 3 representa un bloque destructible

    return grid

# Cargar imágenes de power-ups
def load_power_up_images():
    power_up_images = {}
    for power_up in [BOMB_UP, FIRE_UP, KICK_UP, SPIKE_BOMB]:
        image_path = f"../VSCode/imagenes/bomberman/power_up_{power_up}.png"
        if os.path.exists(image_path):
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (CELL_SIZE, CELL_SIZE))
            power_up_images[power_up] = img
        else:
            print(f"Warning: Image {image_path} not found. Using default color.")
    return power_up_images

POWER_UP_IMAGES = load_power_up_images()


class Player:
    def __init__(self, x, y, color, name):
        self.name = name
        self.x = x
        self.y = y
        self.lastKeyPressed = 'down'
        self.color = color
        self.typeBombs=0
        self.bombs = []
        self.alive = True
        self.max_bombs = 1
        self.fire_power = 2
        self.can_kick = False

    def move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if grid[new_y][new_x] == 0:
                self.x, self.y = new_x, new_y
            elif grid[new_y][new_x] == 2 and self.can_kick:  # Patear bomba
                self.kick_bomb(new_x, new_y, dx, dy, grid)
            elif grid[new_y][new_x] in [BOMB_UP, FIRE_UP, KICK_UP, SPIKE_BOMB]:  # Recoger power-up
                self.collect_powerup(grid[new_y][new_x])
                grid[new_y][new_x] = 0
                self.x, self.y = new_x, new_y

    def place_bomb(self, grid):
        if grid[self.y][self.x] == 0 and len(self.bombs) < self.max_bombs:
            new_bomb = Bomb(self.x, self.y, self.fire_power, self.typeBombs)
            self.bombs.append(new_bomb)

            if self.typeBombs == SPIKE_BOMB:
                grid[self.y][self.x] = 20
            else: 
                grid[self.y][self.x] = 2  # 2 representa una bomba en el grid

    def kick_bomb(self, x, y, dx, dy, grid):
        for bomb in self.bombs:
            if bomb.x == x and bomb.y == y:
                while 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE and grid[y + dy][x + dx] == 0:
                    x, y = x + dx, y + dy
                grid[bomb.y][bomb.x] = 0
                bomb.x, bomb.y = x, y
                grid[bomb.y][bomb.x] = 2
                break

    def collect_powerup(self, powerup):
        if powerup == BOMB_UP:
            self.max_bombs += 1
        elif powerup == FIRE_UP:
            self.fire_power += 1
        elif powerup == KICK_UP:
            self.can_kick = True
        elif powerup == SPIKE_BOMB:
            self.typeBombs = SPIKE_BOMB








class Bomb:
    def __init__(self, x, y, fire_power, typeBombs):
        self.x = x
        self.y = y
        self.typeBombs = typeBombs
        self.timer = 45  # 3 segundos a 30 FPS
        self.fire_power = fire_power
        self.exploding = False
        self.explosion_timer = 15  # 1 segundo de explosión
        self.explosion_cells = []

    def update(self, grid, all_bombs):
        if self.exploding:
            self.explosion_timer -= 1
            return self.explosion_timer <= 0
        else:
            self.timer -= 1
            if self.timer <= 0:
                self.explode(grid, all_bombs)
            return False

    def explode(self, grid, all_bombs):
        grid[self.y][self.x] = 0
        self.exploding = True
        self.create_explosion(grid, all_bombs)

    def create_explosion(self, grid, all_bombs):
        directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(self.fire_power):
                nx, ny = self.x + dx * i, self.y + dy * i
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[ny][nx] == 1:  # Muro indestructible
                        break
                    elif grid[ny][nx] == 3:  # Bloque destructible
                        grid[ny][nx] = 0  # Destruir el bloque
                        self.explosion_cells.append((nx, ny))
                        if random.random() < 0.3:  # 30% de probabilidad de power-up
                            if random.random() < 0.3:  # 50% de probabilidad de que sea una bomba de pinchos
                                grid[ny][nx] = SPIKE_BOMB
                            else:
                                grid[ny][nx] = random.choice([BOMB_UP, FIRE_UP, KICK_UP])
                        if self.typeBombs != SPIKE_BOMB:
                            break
                    elif grid[ny][nx] in [2, 20]:  # Bomba normal o super bomba
                        # Buscar la bomba en all_bombs y hacerla explotar
                        for bomb in all_bombs:
                            if bomb.x == nx and bomb.y == ny and not bomb.exploding:
                                bomb.explode(grid, all_bombs)
                        self.explosion_cells.append((nx, ny))
                    else:
                        self.explosion_cells.append((nx, ny))
                        if self.typeBombs == SPIKE_BOMB:
                            grid[ny][nx] = 40
                        else:
                            grid[ny][nx] = 4  # 4 representa una explosión en el grid



class AIPlayer(Player):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, "IA")
        self.path = []
        self.target = None
        self.move_cooldown = 0
        self.move_speed = 0  # 3 movimientos por segundo (asumiendo 30 FPS)

    def update(self, grid, players):
        if not self.alive:
            return
        global fps
        self.move_cooldown = max(0, self.move_cooldown - 1)

        if not self.path:
            self.choose_target(grid, players)
            if self.target:
                self.path = self.find_path(grid, (self.x, self.y), self.target)
            
            if not self.path:
                self.destroy_nearest_block(grid)

        if self.path and self.move_cooldown == 0:
            next_pos = self.path[0]
            dx, dy = next_pos[0] - self.x, next_pos[1] - self.y
            # Hacemos que espere 1 segundo para hacer el move
            if fps == 0 or fps == 10 or fps == 20:
                if self.move(dx, dy, grid):
                    self.path.pop(0)
                    self.move_cooldown = self.move_speed
                else:
                    self.path = []  # Si no puede moverse, recalcula el camino

        # Colocar bomba si está cerca de un jugador o un bloque destructible
        should_place_bomb = False
        for player in players:
            if player != self and player.alive:
                if abs(self.x - player.x) <= 2 and abs(self.y - player.y) <= 2:
                    should_place_bomb = True
                    break

        if not should_place_bomb:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == 3:
                    should_place_bomb = True
                    break

        if should_place_bomb:
            self.place_bomb(grid)
            # Alejarse de la bomba
            self.path = self.find_safe_spot(grid)

    def choose_target(self, grid, players):
        targets = []
        # Considerar jugadores vivos como objetivos
        for player in players:
            if player != self and player.alive:
                targets.append((player.x, player.y))
        
        # Considerar power-ups como objetivos
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if grid[y][x] in [BOMB_UP, FIRE_UP, KICK_UP, SPIKE_BOMB]:
                    targets.append((x, y))
        
        if targets:
            # Elegir el objetivo más cercano
            self.target = min(targets, key=lambda pos: abs(pos[0] - self.x) + abs(pos[1] - self.y))
        else:
            self.target = None

    def find_path(self, grid, start, goal):
        def heuristic(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - a[1])

        def get_neighbors(pos):
            x, y = pos
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            return [(nx, ny) for nx, ny in neighbors if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] not in [1, 2, 3, 20]]

        heap = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while heap:
            current = heapq.heappop(heap)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heapq.heappush(heap, (f_score[neighbor], neighbor))

        return []

    def find_safe_spot(self, grid):
        queue = deque([(self.x, self.y)])
        visited = set([(self.x, self.y)])
        came_from = {}

        while queue:
            x, y = queue.popleft()
            if grid[y][x] == 0:  # Safe spot found
                path = []
                while (x, y) in came_from:
                    path.append((x, y))
                    x, y = came_from[(x, y)]
                path.reverse()
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] != 1 and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    came_from[(nx, ny)] = (x, y)

        return []  # No safe spot found

    def destroy_nearest_block(self, grid):
        for distance in range(1, max(GRID_SIZE, GRID_SIZE)):
            for dx, dy in [(0, distance), (distance, 0), (0, -distance), (-distance, 0)]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[ny][nx] == 3:  # Bloque destructible
                        # Encuentra una posición adyacente para colocar la bomba
                        for bx, by in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            bomb_x, bomb_y = nx + bx, ny + by
                            if 0 <= bomb_x < GRID_SIZE and 0 <= bomb_y < GRID_SIZE and grid[bomb_y][bomb_x] == 0:
                                # Mueve al jugador a la posición de la bomba
                                path = self.find_path(grid, (self.x, self.y), (bomb_x, bomb_y))
                                if path:
                                    self.path = path
                                    return
        # Si no se encuentra ningún bloque destructible alcanzable, simplemente muévete a una celda vacía adyacente
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == 0:
                self.path = [(nx, ny)]
                return

def create_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    # Añadir muros indestructibles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i % 2 == 0 and j % 2 == 0:
                grid[i][j] = 1

    # Añadir bloques destructibles
    for _ in range(GRID_SIZE * GRID_SIZE // 3):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[y][x] == 0 and (x, y) not in [(1, 1), (1, 2), (2, 1), (GRID_SIZE-2, GRID_SIZE-2), (GRID_SIZE-2, GRID_SIZE-3), (GRID_SIZE-3, GRID_SIZE-2)]:
            grid[y][x] = 3  # 3 representa un bloque destructible

    return grid

def draw_grid(frame, grid):
    # Dibujar el fondo con la textura de suelo
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["suelo"]
            
            if grid[y][x] == 1:  # Muro indestructible
                frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["irrompible"]
            elif grid[y][x] == 2:  # Bomba
                frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["bomba"]
            elif grid[y][x] ==20:  # SpikeBomba
                frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["sbomb"]
            elif grid[y][x] == 3:  # Bloque destructible
                frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["destructible"]
            elif grid[y][x] in [BOMB_UP, FIRE_UP, KICK_UP, SPIKE_BOMB]:  # Power-ups
                if grid[y][x] in POWER_UP_IMAGES:
                    power_up_img = POWER_UP_IMAGES[grid[y][x]]
                    frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = power_up_img
            elif grid[y][x] == 4:  # Explosión
                frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["explosion"]
            elif grid[y][x] == 40:  # Explosión azul (Le ponemos un filtro de color OpenCV)
                    azul = textures["explosion"]
                    azul_hsv = cv2.cvtColor(azul, cv2.COLOR_BGR2HSV)
                    azul_hsv[:, :, 0] = 120  # Cambia el tono (hue) al valor correspondiente al azul
                    azul_azul = cv2.cvtColor(azul_hsv, cv2.COLOR_HSV2BGR)
                    frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = azul_azul


def draw_explosions(frame, bombs):
    for bomb in bombs:
        if bomb.exploding:
            for x, y in bomb.explosion_cells:
                if bomb.typeBombs == SPIKE_BOMB:
                    frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["explosion_blue"]
                else:
                    frame[y*CELL_SIZE:(y+1)*CELL_SIZE, x*CELL_SIZE:(x+1)*CELL_SIZE] = textures["explosion"]


def draw_player(frame, player , player_number):
    # Si es el jugador 1, dibujamos la imagen normal, si es el jugador 2, dibujamos la imagen con un filtro de color, 2 rojo, 3 verde, 4 azul
    if player.alive:
        center = (int((player.x + 0.5) * CELL_SIZE), int((player.y + 0.5) * CELL_SIZE))
        texture = textures[f"{player_number}_{player.lastKeyPressed}"]
        frame[center[1] - CELL_SIZE // 2:center[1] + CELL_SIZE // 2, center[0] - CELL_SIZE // 2:center[0] + CELL_SIZE // 2] = texture

def main():
    print("Selecciona el tipo de mapa:")
    print("1. Mapa generado aleatoriamente")
    print("2. Mapa por defecto (clásico)")
    choice = input("Elige 1 o 2: ")
    random.seed(time.time())
    if choice == '1':
        grid = create_grid()
    elif choice == '2':
        grid = create_default_grid()
    else:
        print("Selección no válida, usando el mapa generado por defecto.")
        grid = create_grid()

    player1 = Player(1, 1, RED, "Jugador 1")
    #player2 = AIPlayer(GRID_SIZE - 2, GRID_SIZE - 2, BLUE)
    player2 = Player(GRID_SIZE - 2, GRID_SIZE - 2, BLUE, "Jugador 2")
    ai_player = AIPlayer(GRID_SIZE - 2, 1, GREEN)  # Nuevo jugador IA

    players = [player1, player2, ai_player]

    while True:
        global fps
        fps += 1
        if fps == 30:
            fps = 0
        frame = np.zeros((WINDOW_SIZE, WINDOW_SIZE, 3), dtype=np.uint8)
        draw_grid(frame, grid)

        # Actualizar y dibujar bombas
        all_bombs = []
        for player in players:
            all_bombs.extend(player.bombs)
            player.bombs = [bomb for bomb in player.bombs if not bomb.update(grid, all_bombs)]

        draw_explosions(frame, all_bombs)

        # Actualizar jugador IA
        ai_player.update(grid, players)
        # Verificar si los jugadores están en una explosión
        for bomb in all_bombs:
            if bomb.exploding:
                for x, y in bomb.explosion_cells:
                    for player in players:
                        if player.x == x and player.y == y:
                            player.alive = False

        # Limpiar explosiones
        grid[grid == 4] = 0
        grid[grid == 40] = 0

        # Dibujar jugadores
        for i, player in enumerate(players, start=1):
            draw_player(frame, player, i)

        cv2.imshow('Bomberman', frame)
        key = cv2.waitKey(33)  # 30 FPS

        # Controles del jugador 1 (WASD + Espacio)
        if key == ord('w'):
            player1.lastKeyPressed = 'up'
            player1.move(0, -1, grid)
        elif key == ord('s'):
            player1.lastKeyPressed = 'down'
            player1.move(0, 1, grid)
        elif key == ord('a'):
            player1.lastKeyPressed = 'left'
            player1.move(-1, 0, grid)
        elif key == ord('d'):
            player1.lastKeyPressed = 'right'
            player1.move(1, 0, grid)
        elif key == ord(' '):
            player1.place_bomb(grid)

        # Controles del jugador 2 (Flechas + Enter)
        elif key == 111:  # Flecha arriba
            player2.lastKeyPressed = 'up'
            player2.move(0, -1, grid)
        elif key == 108:  # Flecha abajo
            player2.lastKeyPressed = 'down'
            player2.move(0, 1, grid)
        elif key == 107:  # Flecha izquierda
            player2.lastKeyPressed = 'left'
            player2.move(-1, 0, grid)
        elif key == 241:  # Flecha derecha
            player2.lastKeyPressed = 'right'
            player2.move(1, 0, grid)
        elif key == 13:  # Enter
            player2.place_bomb(grid)

        elif key == 27:  # ESC
            break

        # Verificar si el juego ha terminado
        alive_players = [player for player in players if player.alive]
        if len(alive_players) <= 1:
            if len(alive_players) == 0:
                print("¡Empate!")
            else:
                if player1.alive:
                    winner = player1.name
                elif player2.alive:
                    winner = player2.name
                elif ai_player.alive:
                    winner = ai_player.name
                print(f"¡{winner} gana!")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()