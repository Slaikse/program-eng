import pygame

class ShadowedText:
    def __init__(self, text, color=(255, 255, 255), font_size=24, shadow_color=(0, 0, 0), offset=(2, 2)):
        self.text = text
        self.color = color
        self.font_size = font_size
        self.shadow_color = shadow_color
        self.offset = offset
        
        # Create font
        self.font = pygame.font.Font(None, font_size)
        
        # Create text surfaces
        self.text_surface = self.font.render(text, True, color)
        self.shadow_surface = self.font.render(text, True, shadow_color)
        
    def draw(self, screen, x, y):
        # Draw shadow
        screen.blit(self.shadow_surface, (x + self.offset[0], y + self.offset[1]))
        # Draw text
        screen.blit(self.text_surface, (x, y)) 