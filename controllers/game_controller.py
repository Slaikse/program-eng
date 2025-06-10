class GameController:
    def __init__(self):
        self.score = 0
        self.moves_left = 0
        self.current_level = None
        self.objectives = {}
        
    def start_level(self, level):
        self.current_level = level
        self.moves_left = level.moves
        self.score = 0
        self.objectives = self.parse_objectives(level.objective)
        
    def parse_objectives(self, objective_list):
        objectives = {}
        for obj in objective_list:
            count, type_ = obj.split(';')
            objectives[type_] = int(count)
        return objectives
    
    def check_objective(self, tile_type):
        if tile_type in self.objectives:
            self.objectives[tile_type] -= 1
            if self.objectives[tile_type] <= 0:
                del self.objectives[tile_type]
            return True
        return False
    
    def add_score(self, points):
        self.score += points
        
    def use_move(self):
        self.moves_left -= 1
        return self.moves_left > 0
    
    def is_level_complete(self):
        return len(self.objectives) == 0
    
    def is_game_over(self):
        return self.moves_left <= 0 and not self.is_level_complete() 