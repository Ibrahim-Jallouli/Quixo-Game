from model.QuixoPiece import QuixoPiece
from model.BoardMemento import BoardMemento

class QuixoBoard:
    def __init__(self):
        # Initialize a 5x5 grid of QuixoPiece instances
        self.grid = [[QuixoPiece() for _ in range(5)] for _ in range(5)]

    def place_piece(self, row, col, player):
        # Place a piece on the board at the specified position 
        self.grid[row][col].mark(player)

    def display(self):
        # Display the current state of the board
        for row in self.grid:
            print(" ".join(str(piece) for piece in row))

    def save_state(self):
        # Save the board's current state as a memento
        return BoardMemento(self.grid)

    def restore_state(self, memento):
        # Restore the board's state from a memento
        self.grid = memento.get_saved_state()