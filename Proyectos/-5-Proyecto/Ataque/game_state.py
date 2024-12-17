
# game_state.py
import time
import cv2

class GameState:
    def __init__(self, config):
        self.config = config
        self.setup_video()
        self.initialize_state()
        
    def setup_video(self):
        self.video = cv2.VideoCapture(self.config.video_path)
        if not self.video.isOpened():
            raise Exception("Error: No se pudo abrir el video")
            
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
    def initialize_state(self):
        if self.config.movement_mode == 'papyrus':
            self.red_dot_pos = [self.width//2, 175]
        else:
            self.red_dot_pos = [self.width//2, self.height//2]
            
        self.running = True
        self.is_moving = False
        self.is_invulnerable = False
        self.invulnerability_start = 0
        self.is_visible = True
        
        # Movement state
        self.vertical_velocity = 0
        self.is_jumping = False
        self.is_grounded = True
        self.jump_held = False
        
        self.keys_pressed = {
            'w': False, 'a': False,
            's': False, 'd': False
        }
        
    def start_invulnerability(self):
        self.is_invulnerable = True
        self.invulnerability_start = time.time()
        
    def update_invulnerability(self):
        if self.is_invulnerable:
            current_time = time.time()
            time_elapsed = current_time - self.invulnerability_start
            
            self.is_visible = int((time_elapsed / self.config.blink_interval) % 2) == 0
            
            if time_elapsed >= self.config.invulnerability_duration:
                self.is_invulnerable = False
                self.is_visible = True
