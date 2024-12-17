# movement_handler.py
import time

class MovementHandler:
    def __init__(self, game_state, config):
        self.game_state = game_state
        self.config = config
        
    def handle_normal_movement(self):
        dx = dy = 0
        if self.game_state.keys_pressed['w']:
            dy -= self.config.movement_speed
        if self.game_state.keys_pressed['s']:
            dy += self.config.movement_speed
        if self.game_state.keys_pressed['a']:
            dx -= self.config.movement_speed
        if self.game_state.keys_pressed['d']:
            dx += self.config.movement_speed

        self.game_state.is_moving = dx != 0 or dy != 0

        if dx != 0 and dy != 0:
            dx = int(dx * 0.707)
            dy = int(dy * 0.707)

        new_x = max(self.config.red_dot_radius, 
                   min(self.game_state.width - self.config.red_dot_radius, 
                       self.game_state.red_dot_pos[0] + dx))
        new_y = max(self.config.red_dot_radius, 
                   min(self.game_state.height - self.config.red_dot_radius, 
                       self.game_state.red_dot_pos[1] + dy))

        self.game_state.red_dot_pos = [new_x, new_y]

    def handle_papyrus_movement(self):
        dx = 0
        if self.game_state.keys_pressed['a']:
            dx -= self.config.movement_speed
        if self.game_state.keys_pressed['d']:
            dx += self.config.movement_speed

        if self.game_state.keys_pressed['w']:
            if self.game_state.is_grounded:
                self.game_state.vertical_velocity = self.config.jump_force
                self.game_state.is_grounded = False
                self.game_state.is_jumping = True
                self.game_state.jump_held = True
            elif self.game_state.is_jumping and self.game_state.jump_held:
                self.game_state.vertical_velocity = max(self.config.max_jump_force, 
                                                      self.game_state.vertical_velocity - 0.15)
                if self.game_state.vertical_velocity > 0:
                    self.game_state.jump_held = False

        if self.game_state.keys_pressed['s'] and not self.game_state.is_grounded:
            self.game_state.vertical_velocity = self.config.fast_fall_speed
            self.game_state.is_jumping = False
            self.game_state.jump_held = False

        if not self.game_state.is_grounded:
            self.game_state.vertical_velocity = min(self.game_state.vertical_velocity + self.config.gravity, 
                                                  self.config.max_fall_speed)

        new_x = max(self.config.red_dot_radius, 
                   min(self.game_state.width - self.config.red_dot_radius, 
                       self.game_state.red_dot_pos[0] + dx))
        new_y = max(self.config.red_dot_radius, 
                   min(self.game_state.height - self.config.red_dot_radius, 
                       self.game_state.red_dot_pos[1] + self.game_state.vertical_velocity))

        if new_y >= self.game_state.height - self.config.red_dot_radius:
            new_y = self.game_state.height - self.config.red_dot_radius
            self.game_state.vertical_velocity = 0
            self.game_state.is_grounded = True
            self.game_state.is_jumping = False

        self.game_state.red_dot_pos = [new_x, int(new_y)]
        self.game_state.is_moving = dx != 0 or self.game_state.vertical_velocity != 0

