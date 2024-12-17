import cv2
import numpy as np
import threading
from pynput import keyboard
import time

class Game:
    def __init__(self, movementMode):
        self.use_opencl = cv2.ocl.haveOpenCL()
        if self.use_opencl:
            # Habilitar OpenCL
            cv2.ocl.setUseOpenCL(True)
            print("OpenCL está disponible. Usando GPU para aceleración.")
            # Obtener información del dispositivo OpenCL
            print("Dispositivo OpenCL:", cv2.ocl.Device.getDefault().name())
        else:
            print("OpenCL no está disponible. Usando CPU.")
            
        self.video = cv2.VideoCapture('./ataques/papyrus/2_processed.avi')
        if not self.video.isOpened():
            raise Exception("Error: No se pudo abrir el video")
            
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if movementMode=='papyrus':
            self.red_dot_pos = [self.width//2, 175]
        else:
            self.red_dot_pos = [self.width//2, self.height//2]
        self.red_dot_radius = 10
        self.movement_speed = 5
        self.running = True
        self.is_moving = False
        self.movementMode=movementMode
        # Variables para el período de invulnerabilidad
        self.is_invulnerable = False
        self.invulnerability_start = 0
        self.invulnerability_duration = 1.0  # 1 segundo de invulnerabilidad
        self.blink_interval = 0.1  # Intervalo de parpadeo en segundos
        self.is_visible = True
        
        # Color del hueso azul de Papyrus (en BGR)
        self.blue_bone_color = np.array([249, 248, 15])  # #0FF8F9 en BGR
        self.blue_threshold = 20  # Tolerancia para detectar el color azul


        
        
        # Variables para el modo Papyrus
        self.gravity = 0.2
        self.jump_force = -3
        self.max_jump_force = -5
        self.max_fall_speed = 15
        self.vertical_velocity = 0
        self.is_jumping = False
        self.is_grounded = True
        self.jump_held = False
        self.fast_fall_speed = 5
        
        
        # Diccionario para mantener el estado de las teclas
        self.keys_pressed = {
            'w': False,
            'a': False,
            's': False,
            'd': False
        }
        self.video_fps = 30  # FPS del video
        self.video_delay = 1 / self.video_fps  # Intervalo entre frames del video
        
    def is_almost_black(self, pixel, threshold=30):
        return np.all(pixel <= threshold)
    
    def is_blue_bone(self, pixel):
        return np.all(np.abs(pixel - self.blue_bone_color) <= self.blue_threshold)
    
    def start_invulnerability(self):
        self.is_invulnerable = True
        self.invulnerability_start = time.time()
        
    def update_invulnerability(self):
        if self.is_invulnerable:
            current_time = time.time()
            time_elapsed = current_time - self.invulnerability_start
            
            # Actualizar visibilidad para el efecto de parpadeo
            self.is_visible = int((time_elapsed / self.blink_interval) % 2) == 0
            
            # Comprobar si el período de invulnerabilidad ha terminado
            if time_elapsed >= self.invulnerability_duration:
                self.is_invulnerable = False
                self.is_visible = True
        
    def handle_movement(self):
        while self.running:
            if self.movementMode == 'normal':
                # Calcular el movimiento basado en las teclas presionadas
                dx = 0
                dy = 0
                if self.keys_pressed['w']:
                    dy -= self.movement_speed
                if self.keys_pressed['s']:
                    dy += self.movement_speed
                if self.keys_pressed['a']:
                    dx -= self.movement_speed
                    print(self.red_dot_pos)
                if self.keys_pressed['d']:
                    dx += self.movement_speed
    
                # Actualizar el estado de movimiento
                self.is_moving = dx != 0 or dy != 0
    
                # Normalizar la velocidad en diagonales
                if dx != 0 and dy != 0:
                    dx = int(dx * 0.707)  # 0.707 ≈ 1/√2
                    dy = int(dy * 0.707)
    
                # Actualizar posición con límites
                new_x = max(self.red_dot_radius, min(self.width - self.red_dot_radius, self.red_dot_pos[0] + dx))
                new_y = max(self.red_dot_radius, min(self.height - self.red_dot_radius, self.red_dot_pos[1] + dy))
    
                self.red_dot_pos = [new_x, new_y]
                time.sleep(1/60)  # Limitar a ~60 actualizaciones por segundo
            elif self.movementMode == 'papyrus':
                dx = 0
    
                # Movimiento horizontal
                if self.keys_pressed['a']:
                    dx -= self.movement_speed
                if self.keys_pressed['d']:
                    dx += self.movement_speed
    
                # Lógica de salto
                if self.keys_pressed['w']:
                    if self.is_grounded:
                        self.vertical_velocity = self.jump_force
                        self.is_grounded = False
                        self.is_jumping = True
                        self.jump_held = True
                    elif self.is_jumping and self.jump_held:
                        # Permitir mantener el salto mientras se mantiene la tecla 'w'
                        self.vertical_velocity = max(self.max_jump_force, self.vertical_velocity - 0.15)
                        if self.vertical_velocity > 0:
                            self.jump_held = False
    
                # Caída rápida con S
                if self.keys_pressed['s'] and not self.is_grounded:
                    self.vertical_velocity = self.fast_fall_speed
                    self.is_jumping = False
                    self.jump_held = False
    
                # Aplicar gravedad
                if not self.is_grounded:
                    self.vertical_velocity = min(self.vertical_velocity + self.gravity, self.max_fall_speed)
    
                # Actualizar posición
                new_x = max(self.red_dot_radius, min(self.width - self.red_dot_radius, self.red_dot_pos[0] + dx))
                new_y = max(self.red_dot_radius, min(self.height - self.red_dot_radius, self.red_dot_pos[1] + self.vertical_velocity))
    
                # Verificar si tocó el suelo
                if new_y >= self.height - self.red_dot_radius:
                    new_y = self.height - self.red_dot_radius
                    self.vertical_velocity = 0
                    self.is_grounded = True
                    self.is_jumping = False
    
                self.red_dot_pos = [new_x, int(new_y)]
                self.is_moving = dx != 0 or self.vertical_velocity != 0
                time.sleep(1/60)
    def on_press(self, key):
        try:
            key_char = key.char.lower()
            if key_char in self.keys_pressed:
                self.keys_pressed[key_char] = True
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            key_char = key.char.lower()
            if key_char in self.keys_pressed:
                self.keys_pressed[key_char] = False
            elif key_char == 'q':
                self.running = False
                return False
        except AttributeError:
            pass

    def run(self):
        # Iniciar thread para el movimiento
        movement_thread = threading.Thread(target=self.handle_movement)
        movement_thread.start()
        
        # Iniciar listener de teclado en un thread separado
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        keyboard_listener.start()

        last_frame_time = 0
        
        while self.running:
            current_time = time.time()
            
            # Actualizar estado de invulnerabilidad
            self.update_invulnerability()
            
            # Solo actualizar el frame del video si ha pasado suficiente tiempo (30 FPS)
            if current_time - last_frame_time >= self.video_delay:
                ret, frame = self.video.read()
                
                if not ret:
                    self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                last_frame_time = current_time  # Actualizar el tiempo del último frame
            
            # Dibujar punto rojo (solo si es visible)
            frame_with_dot = frame.copy()
            if self.is_visible:
                if self.movementMode=='normal':
                    cv2.circle(frame_with_dot, 
                            (self.red_dot_pos[0], self.red_dot_pos[1]), 
                            self.red_dot_radius, 
                            (0, 0, 255), 
                            -1)
                elif self.movementMode=='papyrus':
                    # Normalizamos la altura por que no debe ser float
                    cv2.circle(frame_with_dot, 
                            (self.red_dot_pos[0], self.red_dot_pos[1]), 
                            self.red_dot_radius, 
                            (255, 0, 0), 
                            -1)
                    
                    
                
            # Solo verificar colisiones si no estamos en período de invulnerabilidad
            if not self.is_invulnerable:
                check_radius = self.red_dot_radius
                y_start = max(0, self.red_dot_pos[1] - check_radius)
                y_end = min(self.height, self.red_dot_pos[1] + check_radius + 1)
                x_start = max(0, self.red_dot_pos[0] - check_radius)
                x_end = min(self.width, self.red_dot_pos[0] + check_radius + 1)
                
                check_area = frame[y_start:y_end, x_start:x_end]
                collision = False
                has_blue = False
                
                for y in range(check_area.shape[0]):
                    for x in range(check_area.shape[1]):
                        pixel = check_area[y, x]
                        if self.is_blue_bone(pixel):
                            has_blue = True
                            collision = True
                            break
                        elif not self.is_almost_black(pixel):
                            # Solo registrar colisión si no es un hueso azul
                            if not self.is_blue_bone(pixel):
                                collision = True
                                # Printeamos el color del pixel actual 
                                print(pixel)
                                break
                    if collision:
                        break
                        
                if collision:
                    if has_blue and self.is_moving:
                        print("¡Papyrus daño! ¡No te muevas con los huesos azules!")
                        self.start_invulnerability()
                    elif not has_blue:
                        print("¡Tocaste!")
                        self.start_invulnerability()
            
            # Mostrar el frame con el punto rojo
            cv2.imshow('Juego', frame_with_dot)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        
        self.video.release()
        cv2.destroyAllWindows()
        keyboard_listener.stop()

if __name__ == "__main__":
    game = Game('papyrus')
    game.run()