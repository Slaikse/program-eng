import pygame

class GameLevelButton:
    def __init__(self, x, y, width, height, text, level_number):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.level_number = level_number
        
        # Colors
        self.outer_color = (0, 0, 139)  # Dark blue
        self.inner_color = (0, 0, 255)  # Blue
        self.hover_color = (0, 0, 200)  # Lighter blue for hover
        
        # State
        self.is_hovered = False
        
        # Create the button surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.update_surface()
        
    def update_surface(self):
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw outer rectangle
        pygame.draw.rect(self.surface, self.outer_color, (0, 0, self.width, self.height), border_radius=50)
        
        # Draw inner rectangle
        inner_color = self.hover_color if self.is_hovered else self.inner_color
        pygame.draw.rect(self.surface, inner_color, (2, 2, self.width - 4, self.height - 4), border_radius=48)
        
        # Draw text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)
    
    def update(self):
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.is_clicked(mouse_pos)
        self.update_surface()
    
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y)) 