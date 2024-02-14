class QuixoPiece:
    def __init__(self):
        # Initialize the piece as empty
        self.symbol = ""

    def mark(self, player):
        # Mark the piece with the symbol of the given player
        if self.symbol == "":
            self.symbol = player.symbol

    def __str__(self):
        # String representation of the piece for display purposes
        return self.symbol
