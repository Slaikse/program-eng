import pygame

class TileAnimation:
    def __init__(self, start_pos, end_pos, duration=0.3):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.current_time = 0
        self.is_complete = False
        
    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.duration:
            self.current_time = self.duration
            self.is_complete = True
            
        # Calculate current position using ease-out cubic
        t = self.current_time / self.duration
        t = 1 - (1 - t) * (1 - t) * (1 - t)
        
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
        
        return (x, y)
        
class MatchAnimation:
    def __init__(self, pos, duration=0.5):
        self.pos = pos
        self.duration = duration
        self.current_time = 0
        self.is_complete = False
        
    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.duration:
            self.current_time = self.duration
            self.is_complete = True
            
        # Calculate scale and alpha using ease-out cubic
        t = self.current_time / self.duration
        t = 1 - (1 - t) * (1 - t) * (1 - t)
        
        scale = 1 + t * 0.5
        alpha = 255 * (1 - t)
        
        return scale, alpha
        
class AnimationManager:
    def __init__(self):
        self.animations = []
        self.match_animations = []
        
    def add_tile_animation(self, start_pos, end_pos, tile_type):
        self.animations.append({
            'start_pos': start_pos,
            'end_pos': end_pos,
            'current_pos': list(start_pos),
            'tile_type': tile_type,
            'progress': 0.0
        })
        
    def add_match_animation(self, pos):
        self.match_animations.append({
            'pos': pos,
            'progress': 0.0,
            'scale': 1.0
        })
        
    def update(self, dt):
        # Update tile swap animations
        for anim in self.animations[:]:
            anim['progress'] += dt * 5  # Speed of animation
            if anim['progress'] >= 1.0:
                self.animations.remove(anim)
            else:
                # Linear interpolation between start and end positions
                anim['current_pos'][0] = anim['start_pos'][0] + (anim['end_pos'][0] - anim['start_pos'][0]) * anim['progress']
                anim['current_pos'][1] = anim['start_pos'][1] + (anim['end_pos'][1] - anim['start_pos'][1]) * anim['progress']
        
        # Update match animations
        for anim in self.match_animations[:]:
            anim['progress'] += dt * 3  # Speed of animation
            if anim['progress'] >= 1.0:
                self.match_animations.remove(anim)
            else:
                # Scale effect for match animation
                anim['scale'] = 1.0 + anim['progress'] * 0.5
        
    def draw(self, screen, tile_images, tile_size):
        # Draw tile swap animations
        for anim in self.animations:
            if anim['tile_type'] in tile_images:
                # Draw the tile at its current position
                screen.blit(tile_images[anim['tile_type']], anim['current_pos'])
        
        # Draw match animations
        for anim in self.match_animations:
            # Create a surface for the match effect
            effect_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            # Draw a white circle that fades out
            alpha = int(255 * (1.0 - anim['progress']))
            pygame.draw.circle(effect_surface, (255, 255, 255, alpha), 
                             (tile_size//2, tile_size//2), 
                             int(tile_size//2 * anim['scale']))
            screen.blit(effect_surface, anim['pos']) 