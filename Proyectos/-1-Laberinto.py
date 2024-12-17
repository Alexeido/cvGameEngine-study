import cv2
import numpy as np
import random
import heapq


# Tamaño del laberinto
maze_size = 21  # Debe ser impar para mejor visualización (entrada/salida)
cell_size = 30
width = maze_size * cell_size
height = maze_size * cell_size

# Colores vibrantes
WALL_COLOR = (20, 20, 20)    # Paredes oscuras con apariencia de reflejo
PATH_COLOR = (200, 200, 250) # Suelo reflejando luz suave
PLAYER_COLOR = (50, 200, 50) # Verde claro para el jugador
EXIT_COLOR = (255, 50, 50)   # Rojo brillante para la salida
ENEMY_COLOR = (255, 100, 100) # Enemigo en rojo claro

# Función para generar laberinto usando DFS
def generate_maze(size):
    maze = np.ones((size, size), dtype=np.uint8)

    def dfs(x, y):
        maze[y][x] = 0  # Marca como camino
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # Direcciones posibles
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < size - 1 and 1 <= ny < size - 1 and maze[ny][nx] == 1:
                maze[ny - dy // 2][nx - dx // 2] = 0  # Rompe la pared
                dfs(nx, ny)

    # Empieza el laberinto desde (1, 1)
    dfs(1, 1)
    return maze

# Posición inicial del jugador y enemigo
player_pos = [1, 1]
enemy_pos = [maze_size - 2, maze_size - 2]

# Posición de la salida
exit_pos = [maze_size - 2, maze_size - 2]

# Función para dibujar el laberinto con "Ray Tracing" simulado
def draw_maze(img, maze, player_pos, exit_pos, enemy_pos):
    for i in range(maze_size):
        for j in range(maze_size):
            if maze[i][j] == 1:  # Pared
                color = WALL_COLOR
                # Efecto de "reflejo" en las paredes
                if i % 2 == 0 or j % 2 == 0:
                    color = (min(WALL_COLOR[0] + random.randint(0, 20), 255),
                             min(WALL_COLOR[1] + random.randint(0, 20), 255),
                             min(WALL_COLOR[2] + random.randint(0, 20), 255))
                cv2.rectangle(img, (j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size), color, -1)
            else:  # Camino
                cv2.rectangle(img, (j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size), PATH_COLOR, -1)

    # Dibuja la salida
    cv2.rectangle(img, (exit_pos[1] * cell_size, exit_pos[0] * cell_size),
                  ((exit_pos[1] + 1) * cell_size, (exit_pos[0] + 1) * cell_size), EXIT_COLOR, -1)

    # Dibuja al jugador
    cv2.circle(img, (player_pos[1] * cell_size + cell_size // 2, player_pos[0] * cell_size + cell_size // 2), cell_size // 3, PLAYER_COLOR, -1)

    # Dibuja al enemigo
    cv2.circle(img, (enemy_pos[1] * cell_size + cell_size // 2, enemy_pos[0] * cell_size + cell_size // 2), cell_size // 3, ENEMY_COLOR, -1)

# Función para mover al jugador
def move_player(key, player_pos, maze):
    new_pos = player_pos.copy()
    if key == ord('w'):  # Arriba
        new_pos[0] -= 1
    elif key == ord('s'):  # Abajo
        new_pos[0] += 1
    elif key == ord('a'):  # Izquierda
        new_pos[1] -= 1
    elif key == ord('d'):  # Derecha
        new_pos[1] += 1

    # Verificar si el nuevo movimiento es válido
    if maze[new_pos[0]][new_pos[1]] == 0:
        return new_pos
    return player_pos

# Función heurística (Distancia de Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementación del algoritmo A* para que el enemigo persiga al jugador
def a_star(maze, start, goal):
    # Definimos una lista de posibles movimientos (arriba, abajo, izquierda, derecha)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Cola de prioridad para mantener los nodos por explorar
    heap = []
    heapq.heappush(heap, (0, start))
    
    # Diccionarios para mantener el costo hasta cada nodo y la ruta que se ha seguido
    came_from = {}
    g_score = {start: 0}
    came_from[start] = None

    while heap:
        # Tomamos el nodo con menor costo de la cola de prioridad
        current = heapq.heappop(heap)[1]

        # Si llegamos al objetivo, terminamos
        if current == goal:
            break

        # Recorremos los vecinos del nodo actual
        for neighbor in neighbors:
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            if 0 <= neighbor_pos[0] < maze_size and 0 <= neighbor_pos[1] < maze_size:  # Asegurar que estamos dentro del laberinto
                if maze[neighbor_pos[0]][neighbor_pos[1]] == 1:  # Ignorar las paredes
                    continue

                # Cálculo del nuevo costo
                tentative_g_score = g_score[current] + 1

                if neighbor_pos not in g_score or tentative_g_score < g_score[neighbor_pos]:
                    # Actualizamos el costo y la ruta si es mejor
                    g_score[neighbor_pos] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor_pos, goal)
                    heapq.heappush(heap, (f_score, neighbor_pos))
                    came_from[neighbor_pos] = current

    # Reconstruimos el camino desde el jugador al enemigo
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    
    path.reverse()  # Invertimos para obtener el camino desde el enemigo hasta el jugador

    return path
# Función para añadir una pared
def add_wall(player_pos, maze):
    x, y = player_pos
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for nx, ny in neighbors:
        if 0 <= nx < maze_size and 0 <= ny < maze_size and maze[nx][ny] == 0:
            maze[nx][ny] = 1
            break

# Función para quitar una pared
def remove_wall(player_pos, maze):
    x, y = player_pos
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for nx, ny in neighbors:
        if 0 <= nx < maze_size and 0 <= ny < maze_size and maze[nx][ny] == 1:
            maze[nx][ny] = 0
            break

# Función para mover al enemigo usando A* (inteligencia avanzada)
def move_enemy(player_pos, enemy_pos, maze):
    start = (enemy_pos[0], enemy_pos[1])
    goal = (player_pos[0], player_pos[1])

    # Obtener el camino más corto usando A*
    path = a_star(maze, start, goal)

    # Si el camino no está vacío, el enemigo se mueve hacia la primera posición
    if path:
        next_step = path[0]
        enemy_pos[0] = next_step[0]
        enemy_pos[1] = next_step[1]

    return enemy_pos


# Juego principal
def play_maze():
    global player_pos, enemy_pos

    # Generar laberinto aleatorio
    maze = generate_maze(maze_size)

    # Crear ventana
    cv2.namedWindow("Maze")

    while True:
        # Crear imagen
        img = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Dibujar el laberinto, jugador, salida y enemigo
        draw_maze(img, maze, player_pos, exit_pos, enemy_pos)

        # Mostrar la imagen
        cv2.imshow("Maze", img)

        # Verificar si el jugador llegó a la salida
        if player_pos == exit_pos:
            cv2.putText(img, "¡Ganaste!", (width // 4, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            cv2.imshow("Maze", img)
            cv2.waitKey(3000)
            break

        # Verificar si el enemigo atrapó al jugador
        if player_pos == enemy_pos:
            cv2.putText(img, "¡Perdiste!", (width // 4, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            cv2.imshow("Maze", img)
            cv2.waitKey(3000)
            break

        # Esperar la tecla de movimiento
        key = cv2.waitKey(100)

        # Salir del juego con ESC
        if key == 27:
            break

        # Añadir pared con la tecla 'p'
        if key == ord('p'):
            add_wall(player_pos, maze)

        # Quitar pared con la tecla 'q'
        if key == ord('q'):
            remove_wall(player_pos, maze)

        # Mover jugador
        player_pos = move_player(key, player_pos, maze)

        # Mover enemigo hacia el jugador
        enemy_pos = move_enemy(player_pos, enemy_pos, maze)

    # Cerrar ventana
    cv2.destroyAllWindows()

if __name__ == "__main__":
    play_maze()
