import pygame
import os
from game_widgets.game_level_button import GameLevelButton
from game_widgets.shadowed_text import ShadowedText
from game_widgets.double_curved_container import DoubleCurvedContainer
from animations.shine_effect import ShineEffect
from model.level import Level
from pages.game_page import GamePage

class HomePage:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Load background
        self.background = pygame.image.load(os.path.join('assets', 'images', 'background', 'background2.jpg'))
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Animation properties
        self.animation_value = 0
        self.animation_speed = 0.001
        self.animation_direction = 1
        
        # Create level buttons
        self.level_buttons = []
        self.create_level_buttons()
        
        # Create title container
        title_y = 50
        title_height = 150
        
        # Draw title text
        self.title = ShadowedText(
            text='Три в ряд',
            color=(255, 255, 255),
            font_size=36
        )
        
        # Create copyright text
        self.copyright = ShadowedText(
            text='Powered by Artem Starodubtsev 4309',
            color=(200, 200, 200),
            font_size=16
        )
        
        # Create title container
        self.title_container = DoubleCurvedContainer(
            width=self.width - 60,
            height=150,
            outer_color=(0, 0, 139),  # Dark blue
            inner_color=(0, 0, 255)   # Blue
        )
        
        # Create shine effect
        self.shine_effect = ShineEffect(offset=(100, 100))
        
        # Game state
        self.current_page = self
        self.game_page = None
        
        self.selected_level = None
        
    def create_level_buttons(self):
        button_width = 80
        button_height = 60
        spacing = 20
        buttons_per_row = 3
        
        for i in range(9):  # 9 levels
            row = i // buttons_per_row
            col = i % buttons_per_row
            
            x = (self.width - (button_width * buttons_per_row + spacing * (buttons_per_row - 1))) // 2 + col * (button_width + spacing)
            y = self.height - 300 + row * (button_height + spacing)
            
            button = GameLevelButton(
                x=x,
                y=y,
                width=button_width,
                height=button_height,
                text=f'Уровень {i + 1}',
                level_number=i + 1
            )
            self.level_buttons.append(button)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.level_buttons:
                if button.is_clicked(event.pos):
                    self.selected_level = button.level_number
                    return True
        return False
    
    def update(self):
        # Update animation
        self.animation_value += self.animation_speed * self.animation_direction
        if self.animation_value >= 1:
            self.animation_value = 1
            self.animation_direction = -1
        elif self.animation_value <= 0:
            self.animation_value = 0
            self.animation_direction = 1
            
        # Update shine effect
        self.shine_effect.update()
        
        # Update buttons
        for button in self.level_buttons:
            button.update()
            
        # If we're on the game page, update it
        if self.current_page != self:
            self.current_page.update()
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        if self.current_page == self:
            # Draw title container with animation
            title_y = self.animation_value * 250 - 150
            self.title_container.draw(self.screen, 30, title_y)
            
            # Draw shine effect
            self.shine_effect.draw(self.screen, 30, title_y)
            
            # Draw title text
            self.title.draw(self.screen, self.width // 2, 100)
            
            # Draw copyright
            self.copyright.draw(self.screen, self.width // 2, self.height - 30)
            
            # Draw level buttons
            for button in self.level_buttons:
                button.draw(self.screen)
        else:
            # Draw game page
            self.current_page.draw() 