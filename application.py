import pygame
import sys
from pages.home_page import HomePage
from pages.game_page import GamePage

class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PyMatch3")
        
        self.current_page = HomePage(self.screen)
        self.running = True
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                    
                # Handle page events
                if isinstance(self.current_page, HomePage):
                    # If we're on home page, check for level selection
                    if self.current_page.handle_event(event):
                        # Create new game page with selected level
                        self.current_page = GamePage(self.screen, self.current_page.selected_level)
                else:
                    # If we're on game page, handle game events
                    if self.current_page.handle_event(event):
                        # Return to home page
                        self.current_page = HomePage(self.screen)
            
            # Update current page
            self.current_page.update()
            
            # Draw current page
            self.current_page.draw()
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit() 