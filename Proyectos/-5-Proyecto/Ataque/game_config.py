# game_config.py
class GameConfig:
    def __init__(self, movement_mode='normal', video_path='./ataques/papyrus/4_processed.avi'):
        self.movement_mode = movement_mode
        self.video_path = video_path
        self.video_fps = 30
        self.movement_speed = 5
        self.red_dot_radius = 5
        
        # Gravity and jump settings
        self.gravity = 0.2
        self.jump_force = -3
        self.max_jump_force = -5
        self.max_fall_speed = 15
        self.fast_fall_speed = 5
        
        # Collision settings
        self.blue_bone_color = [249, 248, 15]  # BGR
        self.blue_threshold = 20
        self.black_threshold = 30
        
        # Invulnerability settings
        self.invulnerability_duration = 1.0
        self.blink_interval = 0.1

