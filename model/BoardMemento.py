import copy

class BoardMemento:
    def __init__(self, grid):
        # Take a deep copy of the grid here, not just the reference
        self.saved_grid = copy.deepcopy(grid)

    def get_saved_state(self):
        # Returns a copy of the saved state, just in case
        return copy.deepcopy(self.saved_grid)