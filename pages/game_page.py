import pygame
import os
import random
from model.level import Level
from helpers.audio import Audio
from controllers.game_controller import GameController
from animations.tile_animation import AnimationManager
from animations.particle_system import ParticleSystem

class GamePage:
    def __init__(self, screen, level_number):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Load level
        self.level = Level(level_number)
        
        # Initialize game controller
        self.controller = GameController()
        self.controller.start_level(self.level)
        
        # Game state
        self.selected_tile = None
        self.tile_size = 60
        self.grid_offset_x = (self.width - self.level.grid_size[1] * self.tile_size) // 2
        self.grid_offset_y = (self.height - self.level.grid_size[0] * self.tile_size) // 2
        
        # Create back button
        self.back_button = pygame.Rect(20, 20, 100, 40)
        self.back_font = pygame.font.Font(None, 24)
        
        # Load tile images
        self.tile_images = {}
        self.load_tile_images()
        
        # Load background
        self.background = pygame.image.load(os.path.join('assets', 'images', 'background', 'background2.jpg'))
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
        # Game over state
        self.game_over = False
        self.level_complete = False
        
        # Animation system
        self.animation_manager = AnimationManager()
        self.particle_system = ParticleSystem()
        self.clock = pygame.time.Clock()
        
        # Tile colors for particles
        self.tile_colors = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203),
            'turquoise': (64, 224, 208)
        }
        
        # Check for initial matches and remove them
        self.remove_initial_matches()
        
    def load_tile_images(self):
        tile_types = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'turquoise']
        for tile_type in tile_types:
            try:
                image_path = os.path.join('assets', 'images', 'tiles', f'{tile_type}.png')
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    self.tile_images[tile_type] = pygame.transform.scale(image, (self.tile_size, self.tile_size))
            except:
                print(f"Could not load tile image: {tile_type}")
    
    def get_tile_at_pos(self, pos):
        x, y = pos
        col = (x - self.grid_offset_x) // self.tile_size
        row = (y - self.grid_offset_y) // self.tile_size
        if 0 <= row < self.level.grid_size[0] and 0 <= col < self.level.grid_size[1]:
            return row, col
        return None
    
    def handle_event(self, event):
        if self.game_over or self.level_complete:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Return to home page
                return True
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if back button was clicked
            if self.back_button.collidepoint(event.pos):
                return True
                
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if click is within the game grid area
            grid_rect = pygame.Rect(
                self.grid_offset_x,
                self.grid_offset_y,
                self.level.grid_size[1] * self.tile_size,
                self.level.grid_size[0] * self.tile_size
            )
            
            if grid_rect.collidepoint(mouse_pos):
                tile_pos = self.get_tile_at_pos(mouse_pos)
                if tile_pos:
                    row, col = tile_pos
                    if self.selected_tile is None:
                        self.selected_tile = (row, col)
                        Audio.play_sound('select')
                    else:
                        # Check if tiles are adjacent
                        old_row, old_col = self.selected_tile
                        if (abs(row - old_row) == 1 and col == old_col) or \
                           (abs(col - old_col) == 1 and row == old_row):
                            # Swap tiles
                            self.swap_tiles(old_row, old_col, row, col)
                            Audio.play_sound('swap')
                        self.selected_tile = None
        return False
    
    def remove_initial_matches(self):
        while True:
            matches = self.find_matches()
            if not matches:
                break
            self.process_matches(matches)
            self.fill_empty_spaces()
            
    def fill_empty_spaces(self):
        # Move tiles down
        for col in range(self.level.grid_size[1]):
            empty_spaces = 0
            for row in range(self.level.grid_size[0] - 1, -1, -1):
                if self.level.get_tile_at(row, col) is None:
                    empty_spaces += 1
                elif empty_spaces > 0:
                    # Move tile down
                    new_row = row + empty_spaces
                    self.level.set_tile_at(new_row, col, self.level.get_tile_at(row, col))
                    self.level.set_tile_at(row, col, None)
        
        # Fill top spaces with new tiles
        for col in range(self.level.grid_size[1]):
            for row in range(self.level.grid_size[0]):
                if self.level.get_tile_at(row, col) is None:
                    # Add new random tile
                    tile_types = list(self.tile_colors.keys())
                    self.level.set_tile_at(row, col, random.choice(tile_types))
    
    def swap_tiles(self, row1, col1, row2, col2):
        # Get tile positions
        pos1 = (self.grid_offset_x + col1 * self.tile_size,
                self.grid_offset_y + row1 * self.tile_size)
        pos2 = (self.grid_offset_x + col2 * self.tile_size,
                self.grid_offset_y + row2 * self.tile_size)
        
        # Get tile types
        tile1_type = self.level.get_tile_at(row1, col1)
        tile2_type = self.level.get_tile_at(row2, col2)
        
        # Add swap animation with correct tile types
        self.animation_manager.add_tile_animation(pos1, pos2, tile1_type)
        self.animation_manager.add_tile_animation(pos2, pos1, tile2_type)
        
        # Swap tiles in the level
        self.level.set_tile_at(row1, col1, tile2_type)
        self.level.set_tile_at(row2, col2, tile1_type)
        
        # Check for matches
        matches = self.find_matches()
        if matches:
            # Process matches
            self.process_matches(matches)
            # Use a move
            if not self.controller.use_move():
                self.game_over = True
                Audio.play_sound('lost')
        else:
            # If no matches, swap back
            self.level.set_tile_at(row1, col1, tile1_type)
            self.level.set_tile_at(row2, col2, tile2_type)
            # Add swap back animation
            self.animation_manager.add_tile_animation(pos1, pos2, tile1_type)
            self.animation_manager.add_tile_animation(pos2, pos1, tile2_type)
    
    def find_matches(self):
        matches = set()  # Use set to avoid duplicates
        
        # Check horizontal matches
        for row in range(self.level.grid_size[0]):
            for col in range(self.level.grid_size[1] - 2):
                tile1 = self.level.get_tile_at(row, col)
                tile2 = self.level.get_tile_at(row, col + 1)
                tile3 = self.level.get_tile_at(row, col + 2)
                
                if tile1 and tile2 and tile3 and tile1 == tile2 == tile3:
                    # Add all matching tiles to the set
                    matches.add((row, col))
                    matches.add((row, col + 1))
                    matches.add((row, col + 2))
                    
                    # Check for longer matches
                    col += 3
                    while col < self.level.grid_size[1]:
                        next_tile = self.level.get_tile_at(row, col)
                        if next_tile == tile1:
                            matches.add((row, col))
                            col += 1
                        else:
                            break
        
        # Check vertical matches
        for col in range(self.level.grid_size[1]):
            for row in range(self.level.grid_size[0] - 2):
                tile1 = self.level.get_tile_at(row, col)
                tile2 = self.level.get_tile_at(row + 1, col)
                tile3 = self.level.get_tile_at(row + 2, col)
                
                if tile1 and tile2 and tile3 and tile1 == tile2 == tile3:
                    # Add all matching tiles to the set
                    matches.add((row, col))
                    matches.add((row + 1, col))
                    matches.add((row + 2, col))
                    
                    # Check for longer matches
                    row += 3
                    while row < self.level.grid_size[0]:
                        next_tile = self.level.get_tile_at(row, col)
                        if next_tile == tile1:
                            matches.add((row, col))
                            row += 1
                        else:
                            break
        
        return list(matches)
    
    def process_matches(self, matches):
        # Process each match
        for row, col in matches:
            # Add match animation
            pos = (self.grid_offset_x + col * self.tile_size,
                   self.grid_offset_y + row * self.tile_size)
            self.animation_manager.add_match_animation(pos)
            
            # Add particles
            tile_type = self.level.get_tile_at(row, col)
            if tile_type in self.tile_colors:
                self.particle_system.emit(
                    pos[0] + self.tile_size // 2,
                    pos[1] + self.tile_size // 2,
                    self.tile_colors[tile_type],
                    count=20
                )
            
            # Clear the matched tile
            self.level.set_tile_at(row, col, None)
            
            # Add points for each match
            self.controller.add_score(10)
            
            # Add bonus points for objective matches
            if self.controller.check_objective(tile_type):
                self.controller.add_score(100)
                Audio.play_sound('match')
        
        # Fill empty spaces and check for new matches
        self.fill_empty_spaces()
        new_matches = self.find_matches()
        if new_matches:
            self.process_matches(new_matches)
        
        # Check if level is complete
        if self.level.level_number == 1 and self.controller.score >= 100:
            self.level_complete = True
            Audio.play_sound('win')
            # Emit victory particles
            for _ in range(5):
                self.particle_system.emit(
                    self.width // 2,
                    self.height // 2,
                    (255, 215, 0),  # Gold color
                    count=30
                )
        elif self.level.level_number == 2 and self.controller.score >= 1000:
            self.level_complete = True
            Audio.play_sound('win')
            # Emit victory particles
            for _ in range(5):
                self.particle_system.emit(
                    self.width // 2,
                    self.height // 2,
                    (255, 215, 0),  # Gold color
                    count=30
                )
        elif self.level.level_number > 2 and self.controller.is_level_complete():
            self.level_complete = True
            Audio.play_sound('win')
            # Emit victory particles
            for _ in range(5):
                self.particle_system.emit(
                    self.width // 2,
                    self.height // 2,
                    (255, 215, 0),  # Gold color
                    count=30
                )
    
    def update(self):
        # Update animations
        dt = self.clock.tick(60) / 1000.0  # Convert to seconds
        self.animation_manager.update(dt)
        self.particle_system.update(dt)
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw grid
        for row in range(self.level.grid_size[0]):
            for col in range(self.level.grid_size[1]):
                tile_type = self.level.get_tile_at(row, col)
                if tile_type in self.tile_images:
                    x = self.grid_offset_x + col * self.tile_size
                    y = self.grid_offset_y + row * self.tile_size
                    self.screen.blit(self.tile_images[tile_type], (x, y))
                    
                    # Draw selection highlight
                    if self.selected_tile == (row, col):
                        pygame.draw.rect(self.screen, (255, 255, 0), 
                                       (x, y, self.tile_size, self.tile_size), 3)
        
        # Draw animations
        self.animation_manager.draw(self.screen, self.tile_images, self.tile_size)
        
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Draw back button
        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button)
        back_text = self.back_font.render('Назад', True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw game stats
        if self.level.level_number == 1:
            score_text = self.font.render(f'Счёт: {self.controller.score}/100', True, (255, 255, 255))
            moves_text = self.font.render(f'Ходы: {self.controller.moves_left}', True, (255, 255, 255))
            self.screen.blit(score_text, (20, 70))
            self.screen.blit(moves_text, (20, 110))
        elif self.level.level_number == 2:
            score_text = self.font.render(f'Счёт: {self.controller.score}/1000', True, (255, 255, 255))
            moves_text = self.font.render(f'Ходы: {self.controller.moves_left}', True, (255, 255, 255))
            self.screen.blit(score_text, (20, 70))
            self.screen.blit(moves_text, (20, 110))
        else:
            score_text = self.font.render(f'Счёт: {self.controller.score}', True, (255, 255, 255))
            moves_text = self.font.render(f'Ходы: {self.controller.moves_left}', True, (255, 255, 255))
            self.screen.blit(score_text, (20, 70))
            self.screen.blit(moves_text, (20, 110))
            
            # Draw objectives (excluding bombs and flares)
            y = 150
            for obj_type, count in self.controller.objectives.items():
                if 'bomb' not in obj_type.lower() and 'flare' not in obj_type.lower():  # Skip bomb and flare objectives
                    obj_text = self.font.render(f'{obj_type}: {count}', True, (255, 255, 255))
                    self.screen.blit(obj_text, (20, y))
                    y += 40
        
        # Draw game over or level complete message
        if self.game_over:
            self.draw_message("Игра окончена!", (255, 0, 0))
        elif self.level_complete:
            if self.level.level_number == 1 and self.controller.score >= 100:
                self.level_complete = True
                self.draw_message("Уровень пройден!", (0, 255, 0))
            elif self.level.level_number == 2 and self.controller.score >= 1000:
                self.level_complete = True
                self.draw_message("Уровень пройден!", (0, 255, 0))
            elif self.level.level_number > 2:
                self.level_complete = True
                self.draw_message("Уровень пройден!", (0, 255, 0))
    
    def draw_message(self, text, color):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw message
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Draw click to continue message
        continue_text = self.font.render("Нажмите для продолжения", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(continue_text, continue_rect) 