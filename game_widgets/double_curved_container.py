import pygame

class DoubleCurvedContainer:
    def __init__(self, width, height, outer_color=(0, 0, 139), inner_color=(0, 0, 255)):
        self.width = width
        self.height = height
        self.outer_color = outer_color
        self.inner_color = inner_color
        
        # Create the container surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.update_surface()
        
    def update_surface(self):
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw outer rectangle with curved edges
        pygame.draw.rect(self.surface, self.outer_color, (0, 0, self.width, self.height), border_radius=20)
        
        # Draw inner rectangle with curved edges
        pygame.draw.rect(self.surface, self.inner_color, (2, 2, self.width - 4, self.height - 4), border_radius=18)
        
    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y)) 