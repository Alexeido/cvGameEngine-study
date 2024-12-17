import cv2
import numpy as np
import math
import random

# Configuración
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = 800
CELL_SIZE = 64
PLAYER_SIZE = 10
ENEMY_SIZE = 32
NUM_ENEMIES = 3

# Función para generar mapa aleatorio
def generate_random_map(width, height):
    map = [[1 for _ in range(width)] for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() > 0.3:  # 70% de probabilidad de espacio vacío
                map[y][x] = 0
    map[1][1] = 0
    return map

# Pedir dimensiones del mapa al usuario
map_width = int(input("Introduce el ancho del mapa: "))
map_height = int(input("Introduce el alto del mapa: "))

# Generar mapa aleatorio
MAP = generate_random_map(map_width, map_height)

# Ajustar posición inicial del jugador
player_x, player_y = CELL_SIZE * 1.5, CELL_SIZE * 1.5
player_angle = 0

# Lista de enemigos: [x, y, alive]
enemies = []

# Cargar imagen del enemigo
try:
    enemy_image = cv2.imread('../VSCode/imagenes/enemy.png', cv2.IMREAD_UNCHANGED)
    if enemy_image is None:
        raise FileNotFoundError("No se pudo cargar 'enemy.png'")
    
    if enemy_image.shape[2] != 4:
        enemy_image = cv2.cvtColor(enemy_image, cv2.COLOR_BGR2BGRA)
    
    enemy_image = cv2.resize(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
except Exception as e:
    print(f"Error al cargar la imagen del enemigo: {e}")
    print("Usando un círculo rojo como representación del enemigo.")
    enemy_image = np.zeros((ENEMY_SIZE, ENEMY_SIZE, 4), dtype=np.uint8)
    cv2.circle(enemy_image, (ENEMY_SIZE//2, ENEMY_SIZE//2), ENEMY_SIZE//2, (0, 0, 255, 255), -1)

# Pistola
gun_image = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
cv2.rectangle(gun_image, (WIDTH//2 - 20, HEIGHT - 100), (WIDTH//2 + 20, HEIGHT), (100, 100, 100), -1)
cv2.rectangle(gun_image, (WIDTH//2 - 10, HEIGHT - 80), (WIDTH//2 + 10, HEIGHT - 20), (50, 50, 50), -1)

def init_enemies():
    global enemies
    enemies = []
    for _ in range(NUM_ENEMIES):
        while True:
            x = random.randint(1, len(MAP[0])-2) * CELL_SIZE + CELL_SIZE // 2
            y = random.randint(1, len(MAP)-2) * CELL_SIZE + CELL_SIZE // 2
            if MAP[int(y // CELL_SIZE)][int(x // CELL_SIZE)] == 0:
                enemies.append([x, y, True])
                break
    print(f"Enemigos inicializados: {enemies}")

def distance(ax, ay, bx, by):
    return math.sqrt((bx - ax)**2 + (by - ay)**2)


def cast_rays():
    start_angle = player_angle - HALF_FOV
    
    rendered_enemies = set()  # Conjunto para almacenar los enemigos ya renderizados

    for ray in range(CASTED_RAYS):
        closest_enemy = None
        closest_enemy_dist = float('inf')

        for depth in range(MAX_DEPTH):
            target_x = player_x + math.cos(start_angle) * depth
            target_y = player_y + math.sin(start_angle) * depth
            
            col = int(target_x / CELL_SIZE)
            row = int(target_y / CELL_SIZE)
            
            if MAP[row][col] == 1:
                color = 255 / (1 + depth * depth * 0.0001)
                depth *= math.cos(player_angle - start_angle)
                wall_height = 21000 / (depth + 0.0001)
                
                if wall_height > HEIGHT:
                    wall_height = HEIGHT
                    
                cv2.line(frame, (ray * int(WIDTH / CASTED_RAYS), int(HEIGHT / 2 - wall_height / 2)),
                         (ray * int(WIDTH / CASTED_RAYS), int(HEIGHT / 2 + wall_height / 2)), (color, color, color), 1)
                break
        
        for enemy in enemies:
            if enemy[2] and tuple(enemy) not in rendered_enemies:  # Convertir a tupla para que sea hashable
                enemy_x, enemy_y = enemy[0], enemy[1]
                distance_to_enemy = distance(player_x, player_y, enemy_x, enemy_y)
                angle_to_enemy = math.atan2(enemy_y - player_y, enemy_x - player_x)

                if abs(angle_to_enemy - start_angle) < 0.1 and distance_to_enemy < depth:
                    if distance_to_enemy < closest_enemy_dist:
                        closest_enemy = enemy
                        closest_enemy_dist = distance_to_enemy

        if closest_enemy and tuple(closest_enemy) not in rendered_enemies:
            enemy_height = int(15000 / (closest_enemy_dist + 0.0001))
            if enemy_height > HEIGHT:
                enemy_height = HEIGHT
            
            enemy_width = int(enemy_height * enemy_image.shape[1] / enemy_image.shape[0])
            if enemy_width > 0 and enemy_height > 0:
                try:
                    scaled_enemy = cv2.resize(enemy_image, (enemy_width, enemy_height))
                
                    pos_x = ray * int(WIDTH / CASTED_RAYS) - int(enemy_width / 2)
                    pos_y = int(HEIGHT / 2 - enemy_height / 2)
                    
                    if pos_x < 0:
                        scaled_enemy = scaled_enemy[:, -pos_x:]
                        pos_x = 0
                    if pos_x + scaled_enemy.shape[1] > WIDTH:
                        scaled_enemy = scaled_enemy[:, :WIDTH-pos_x]
                    if pos_y < 0:
                        scaled_enemy = scaled_enemy[-pos_y:, :]
                        pos_y = 0
                    if pos_y + scaled_enemy.shape[0] > HEIGHT:
                        scaled_enemy = scaled_enemy[:HEIGHT-pos_y, :]
                    
                    if scaled_enemy.shape[2] == 4:  # Si tiene canal alpha
                        alpha_s = scaled_enemy[:, :, 3] / 255.0
                        alpha_l = 1.0 - alpha_s
                        for c in range(0, 3):
                            frame[pos_y:pos_y+scaled_enemy.shape[0], pos_x:pos_x+scaled_enemy.shape[1], c] = \
                                (alpha_s * scaled_enemy[:, :, c] + alpha_l * frame[pos_y:pos_y+scaled_enemy.shape[0], pos_x:pos_x+scaled_enemy.shape[1], c])
                    else:
                        frame[pos_y:pos_y+scaled_enemy.shape[0], pos_x:pos_x+scaled_enemy.shape[1]] = scaled_enemy

                    # Añadir enemigo al conjunto de renderizados
                    rendered_enemies.add(tuple(closest_enemy))  # Convertimos a tupla aquí también

                except Exception as e:
                    print(f"Error al renderizar enemigo: {e}")
        
        start_angle += STEP_ANGLE

def draw_minimap(scale=0.2):
    minimap_size = int(min(WIDTH, HEIGHT) * scale)
    minimap = np.zeros((minimap_size, minimap_size, 3), dtype=np.uint8)
    
    cell_size = minimap_size // max(len(MAP), len(MAP[0]))
    
    for y, row in enumerate(MAP):
        for x, cell in enumerate(row):
            if cell == 1:
                cv2.rectangle(minimap, (x * cell_size, y * cell_size), 
                              ((x + 1) * cell_size, (y + 1) * cell_size), (200, 200, 200), -1)
    
    player_minimap_x = int(player_x / CELL_SIZE * cell_size)
    player_minimap_y = int(player_y / CELL_SIZE * cell_size)
    cv2.circle(minimap, (player_minimap_x, player_minimap_y), 2, (0, 255, 0), -1)
    
    for enemy in enemies:
        if enemy[2]:  # Si el enemigo está vivo
            enemy_minimap_x = int(enemy[0] / CELL_SIZE * cell_size)
            enemy_minimap_y = int(enemy[1] / CELL_SIZE * cell_size)
            cv2.circle(minimap, (enemy_minimap_x, enemy_minimap_y), 2, (0, 0, 255), -1)
    
    frame[10:10+minimap_size, 10:10+minimap_size] = minimap

import heapq
import random
import math

def heuristic(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

def get_neighbors(node, map):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < len(map[0]) and 0 <= ny < len(map) and map[ny][nx] == 0:
            neighbors.append((nx, ny))
    return neighbors

def a_star(start, goal, map):
    start = (int(start[0] // CELL_SIZE), int(start[1] // CELL_SIZE))
    goal = (int(goal[0] // CELL_SIZE), int(goal[1] // CELL_SIZE))
    
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in get_neighbors(current, map):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    if goal not in came_from:
        return None

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def move_enemies():
    global enemies
    for enemy in enemies:
        if enemy[2]:  # Si el enemigo está vivo
            # Calcular la ruta hacia el jugador
            start = (enemy[0], enemy[1])
            goal = (player_x, player_y)
            path = a_star(start, goal, MAP)

            if path and len(path) > 1:
                # Movimiento lento: 50% de probabilidad de moverse en cada frame
                random.seed()
                posibilidad= random.random()
                if posibilidad < 0.01:
                    next_pos = path[1]
                    new_x = next_pos[0] * CELL_SIZE + CELL_SIZE // 5
                    new_y = next_pos[1] * CELL_SIZE + CELL_SIZE // 5

                    # Añadir un poco de aleatoriedad al movimiento, elegiremos un valor entre -1 y 1 y luego a que direccion lo hará

                    new_x += random.randint(-1, 1)
                    new_y += random.randint(-1, 1)

                    # Asegurarse de que el nuevo movimiento no atraviese paredes
                    if MAP[int(new_y // CELL_SIZE)][int(new_x // CELL_SIZE)] == 0:
                        enemy[0] = new_x
                        enemy[1] = new_y

    # Verificar si todos los enemigos han sido eliminados
    if all(not enemy[2] for enemy in enemies):
        print("¡Has eliminado a todos los enemigos!")
        init_enemies()

def shoot():
    for enemy in enemies:
        if enemy[2]:  # Si el enemigo está vivo
            enemy_x, enemy_y = enemy[0], enemy[1]
            distance_to_enemy = distance(player_x, player_y, enemy_x, enemy_y)
            angle_to_enemy = math.atan2(enemy_y - player_y, enemy_x - player_x)
            
            if abs(angle_to_enemy - player_angle) < 0.1 and distance_to_enemy < MAX_DEPTH:
                enemy[2] = False  # Marcar el enemigo como eliminado
                return True
    return False

init_enemies()

while True:
    frame = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
    cast_rays()
    
    move_enemies()
    
    # Dibujar la pistola
    frame = cv2.addWeighted(frame, 1, gun_image, 0.5, 0)
    
    # Dibujar el minimapa
    draw_minimap()
    
    cv2.imshow('Doom-like', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('a'):
        player_angle -= 0.1
    if key == ord('d'):
        player_angle += 0.1
    if key == ord('w'):
        new_x = player_x + math.cos(player_angle) * 5
        new_y = player_y + math.sin(player_angle) * 5
        if MAP[int(new_y // CELL_SIZE)][int(new_x // CELL_SIZE)] == 0:
            player_x, player_y = new_x, new_y
    if key == ord('s'):
        new_x = player_x - math.cos(player_angle) * 5
        new_y = player_y - math.sin(player_angle) * 5
        if MAP[int(new_y // CELL_SIZE)][int(new_x // CELL_SIZE)] == 0:
            player_x, player_y = new_x, new_y
    if key == ord(' '):  # Espacio para disparar
        if shoot():
            print("¡Enemigo eliminado!")
    if key == ord('q'):
        break

cv2.destroyAllWindows()