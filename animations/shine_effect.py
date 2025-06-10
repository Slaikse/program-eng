import pygame
import math

class ShineEffect:
    def __init__(self, offset=(100, 100)):
        self.offset = offset
        self.angle = 0
        self.speed = 0.02
        self.radius = 50
        self.opacity = 128
        
    def update(self):
        # Update angle
        self.angle += self.speed
        if self.angle > 2 * math.pi:
            self.angle = 0
            
    def draw(self, screen, x, y):
        # Calculate shine position
        shine_x = x + self.offset[0] + math.cos(self.angle) * self.radius
        shine_y = y + self.offset[1] + math.sin(self.angle) * self.radius
        
        # Create shine surface
        shine_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        
        # Draw gradient circle
        for r in range(50, 0, -1):
            alpha = int(self.opacity * (1 - r/50))
            color = (255, 255, 255, alpha)
            pygame.draw.circle(shine_surface, color, (50, 50), r)
            
        # Draw shine
        screen.blit(shine_surface, (shine_x - 50, shine_y - 50)) 