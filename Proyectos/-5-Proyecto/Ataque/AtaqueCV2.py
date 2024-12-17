# main.py
import cv2
import threading
from pynput import keyboard
import time
from Ataque.game_config import GameConfig
from Ataque.game_state import GameState
from Ataque.movement_handler import MovementHandler
from Ataque.collision_handler import CollisionHandler

dirAttacks='./ataques/'

class Game:
    def __init__(self, movement_mode='normal', attack='/papyrus/4_processed.avi'):
        self.config = GameConfig(movement_mode, dirAttacks+attack)
        self.game_state = GameState(self.config)
        self.movement_handler = MovementHandler(self.game_state, self.config)
        self.hits=0
        self.collision_handler = CollisionHandler(self.game_state, self.config, self.hits)
        self.running = True  # Control general para detener el juego

    def handle_movement(self):
        while self.game_state.running and self.running:
            if self.config.movement_mode == 'normal':
                self.movement_handler.handle_normal_movement()
            else:
                self.movement_handler.handle_papyrus_movement()
            time.sleep(1/60)

    def on_press(self, key):
        try:
            key_char = key.char.lower()
            if key_char in self.game_state.keys_pressed:
                self.game_state.keys_pressed[key_char] = True
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            key_char = key.char.lower()
            if key_char in self.game_state.keys_pressed:
                self.game_state.keys_pressed[key_char] = False
            elif key_char == 'q':
                self.game_state.running = False
                self.running = False  # Para detener todos los hilos
                return False
        except AttributeError:
            pass

    def run(self):
        # Thread para manejar el movimiento
        movement_thread = threading.Thread(target=self.handle_movement, daemon=True)
        movement_thread.start()
        
        # Listener de teclado
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        keyboard_listener.start()
    
        last_frame_time = 0
        video_delay = 1 / self.config.video_fps
        
        while self.game_state.running and self.running:
            current_time = time.time()
            
            self.game_state.update_invulnerability()
            
            if current_time - last_frame_time >= video_delay:
                ret, frame = self.game_state.video.read()
                
                if not ret:
                    # Final del video, detiene el juego
                    self.game_state.running = False
                    self.running = False
                    break
                
                last_frame_time = current_time
            
            frame_with_dot = frame.copy()
            if self.game_state.is_visible:
                color = (255, 0, 0) if self.config.movement_mode == 'papyrus' else (0, 0, 255)
                cv2.circle(frame_with_dot, 
                          (self.game_state.red_dot_pos[0], self.game_state.red_dot_pos[1]), 
                          self.config.red_dot_radius, 
                          color,
                          -1)
            
            self.collision_handler.check_collisions(frame)
            
            cv2.imshow('Juego', frame_with_dot)
            
            # Escucha tecla 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.game_state.running = False
                self.running = False
                break
        
        # Limpieza al terminar el juego
        self.cleanup(keyboard_listener)

    def cleanup(self, keyboard_listener):
        # Liberar video y cerrar ventanas de OpenCV
        self.hits=self.collision_handler.hits
        self.game_state.video.release()
        self.game_state.running = False
        self.running = False
        cv2.destroyWindow('Juego')

        
        # Detener el listener del teclado de manera segura
        keyboard_listener.stop()
        keyboard_listener.join()
        return self.hits

if __name__ == "__main__":
    game = Game('papyrus', '/papyrus/2_processed.avi')
    game.run()
