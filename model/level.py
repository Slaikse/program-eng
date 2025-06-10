import json
import os
import random

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.grid_size = (8, 8)  # Default grid size
        self.target_score = 1000
        self.moves = 30
        self.tiles = []
        self.objective = []  # Add objective attribute
        self.load_level()
        
    def load_level(self):
        try:
            with open(os.path.join('assets', 'levels.json'), 'r') as f:
                levels_data = json.load(f)
                # Find the level data in the levels array
                level_data = next((level for level in levels_data['levels'] 
                                 if level['level'] == self.level_number), None)
                
                if level_data:
                    self.grid_size = (level_data.get('rows', 8), level_data.get('cols', 8))
                    self.moves = level_data.get('moves', 30)
                    self.objective = level_data.get('objective', [])
                    
                    # Convert grid data to tiles
                    grid = level_data.get('grid', [])
                    self.tiles = []
                    tile_types = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'turquoise']
                    
                    for row in grid:
                        # Split row by comma and convert to tile types
                        row_tiles = []
                        for cell in row.split(','):
                            if cell == '1':
                                # Randomly assign a tile type
                                row_tiles.append(random.choice(tile_types))
                            elif cell == 'X':
                                row_tiles.append(None)  # Empty cell
                            elif cell == 'W':
                                row_tiles.append('blue')  # Wall cell
                            elif cell == '2':
                                row_tiles.append('green')  # Special cell
                            else:
                                row_tiles.append(random.choice(tile_types))
                        self.tiles.extend(row_tiles)
                else:
                    # Use default values if level not found
                    self.tiles = ['red', 'blue', 'green', 'yellow', 'purple'] * (self.grid_size[0] * self.grid_size[1])
                    self.objective = ["4;blue", "20;red"]  # Default objectives
                    
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            # Use default values if level file is not found or invalid
            self.tiles = ['red', 'blue', 'green', 'yellow', 'purple'] * (self.grid_size[0] * self.grid_size[1])
            self.objective = ["4;blue", "20;red"]  # Default objectives
            
    def get_tile_at(self, row, col):
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            index = row * self.grid_size[1] + col
            return self.tiles[index]
        return None
        
    def set_tile_at(self, row, col, tile_type):
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            index = row * self.grid_size[1] + col
            self.tiles[index] = tile_type 