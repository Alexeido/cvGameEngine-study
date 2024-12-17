# collision_handler.py
import numpy as np

class CollisionHandler:
    def __init__(self, game_state, config, hits):
        self.hits=hits
        self.game_state = game_state
        self.config = config
    
    def is_almost_black(self, pixel):
        return np.all(pixel <= self.config.black_threshold)
    
    def is_blue_bone(self, pixel):
        return np.all(np.abs(pixel - np.array(self.config.blue_bone_color)) <= self.config.blue_threshold)
    
    def check_collisions(self, frame):
        if not self.game_state.is_invulnerable:
            check_radius = self.config.red_dot_radius
            y_start = max(0, self.game_state.red_dot_pos[1] - check_radius)
            y_end = min(self.game_state.height, self.game_state.red_dot_pos[1] + check_radius + 1)
            x_start = max(0, self.game_state.red_dot_pos[0] - check_radius)
            x_end = min(self.game_state.width, self.game_state.red_dot_pos[0] + check_radius + 1)
            
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
                    elif not self.is_almost_black(pixel) and not self.is_blue_bone(pixel):
                        collision = True
                        break
                if collision:
                    break
            
            if collision:
                if has_blue and self.game_state.is_moving:
                    print("¡Papyrus daño! ¡No te muevas con los huesos azules!")
                    self.hits += 1
                    self.game_state.start_invulnerability()
                elif not has_blue:
                    print("¡Tocaste!")
                    self.hits += 1
                    self.game_state.start_invulnerability()
