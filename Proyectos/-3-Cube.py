import cv2
import numpy as np

# Definir puntos del cubo 3D
cubo_puntos = np.float32([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
])

# Definir caras del cubo con índices a los puntos
caras = [
    [0, 1, 2, 3],  # Cara trasera
    [4, 5, 6, 7],  # Cara delantera
    [0, 1, 5, 4],  # Cara inferior
    [2, 3, 7, 6],  # Cara superior
    [0, 3, 7, 4],  # Cara izquierda
    [1, 2, 6, 5]   # Cara derecha
]

# Colores de las caras
colores_caras = [
    (255, 0, 0),    # Rojo
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarillo
    (255, 0, 255),  # Magenta
    (0, 255, 255)   # Cian
]

# Función de proyección 3D a 2D
def proyectar(punto, angulo_x, angulo_y, angulo_z, escala, centro):
    # Matrices de rotación
    rot_x = np.array([
        [1, 0, 0],
        [0, np.cos(angulo_x), -np.sin(angulo_x)],
        [0, np.sin(angulo_x), np.cos(angulo_x)]
    ])
    
    rot_y = np.array([
        [np.cos(angulo_y), 0, np.sin(angulo_y)],
        [0, 1, 0],
        [-np.sin(angulo_y), 0, np.cos(angulo_y)]
    ])
    
    rot_z = np.array([
        [np.cos(angulo_z), -np.sin(angulo_z), 0],
        [np.sin(angulo_z), np.cos(angulo_z), 0],
        [0, 0, 1]
    ])
    
    # Rotar el punto
    rotado = np.dot(punto, rot_x)
    rotado = np.dot(rotado, rot_y)
    rotado = np.dot(rotado, rot_z)
    
    # Proyectar el punto en 2D
    proyectado = rotado[:2] * escala + centro
    return proyectado.astype(int)

# Función para dibujar caras coloreadas del cubo
def dibujar_cubo(img, puntos_2d):
    for i, cara in enumerate(caras):
        puntos = np.array([puntos_2d[j] for j in cara])
        cv2.fillConvexPoly(img, puntos, colores_caras[i])

# Variables de estado
angulo_x, angulo_y, angulo_z = 0, 0, 0
escala = 200
centro = (320, 240)
moviendo = False
ultimo_x, ultimo_y = 0, 0

# Eventos de ratón
def mover_cubo(evento, x, y, flags, param):
    global angulo_x, angulo_y, moviendo, ultimo_x, ultimo_y, escala
    if evento == cv2.EVENT_LBUTTONDOWN:
        moviendo = True
        ultimo_x, ultimo_y = x, y
    elif evento == cv2.EVENT_LBUTTONUP:
        moviendo = False
    elif evento == cv2.EVENT_MOUSEMOVE and moviendo:
        dx = x - ultimo_x
        dy = y - ultimo_y
        angulo_y += dx * 0.01
        angulo_x += dy * 0.01
        ultimo_x, ultimo_y = x, y
    elif evento == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            escala += 20  # Zoom in
        else:
            escala -= 20  # Zoom out
        escala = max(100, min(500, escala))  # Limitar el zoom

# Crear una ventana y asignar el evento del ratón
cv2.namedWindow('Cubo 3D')
cv2.setMouseCallback('Cubo 3D', mover_cubo)

while True:
    # Crear una imagen en blanco
    imagen = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Proyectar puntos 3D a 2D
    puntos_2d = [proyectar(p, angulo_x, angulo_y, angulo_z, escala, centro) for p in cubo_puntos]
    
    # Dibujar el cubo con las caras coloreadas
    dibujar_cubo(imagen, puntos_2d)
    
    # Mostrar la imagen
    cv2.imshow('Cubo 3D', imagen)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
