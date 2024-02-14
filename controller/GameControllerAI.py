from controller.GameController import GameController
from model.AIPlayer import AIPlayer
from concurrent.futures import ThreadPoolExecutor

class GameControllerAI(GameController):
    def __init__(self):
        super().__init__()
        self.player2 = AIPlayer("O")

    def get_ai_move(self):
        best_score = float('-inf')  # Initialize to negative infinity
        best_move = None

        possible_selections = self.get_possible_selections()

        for selection in possible_selections:
            row, col = selection
            possible_positions = self.get_possible_positions(row, col)
            
            for position in possible_positions:
                target_row, target_col = position

                # Simulate the move and evaluate the score using Minimax
                self.make_move(row, col, target_row, target_col)
                print("selection : ",selection)
                print("position : ",position)
                score = self.minimax(0, False)
                self.undo()  # Revert the simulated move

                # Update the best move if a higher score is found
                if score > best_score:
                    best_score = score
                    best_move = (row, col, target_row, target_col)
                    
        return best_move

    def minimax(self, depth, is_maximizing_player):
        game_over, winner, _ = self.is_game_over()

        if depth == 0 or game_over :
            print("evaluation : ",self.evaluate())
            print()
            return self.evaluate()

        if is_maximizing_player:
            best_score = float('-inf')  # Initialize to negative infinity
            for selection in self.get_possible_selections():
                row, col = selection
                possible_positions = self.get_possible_positions(row, col)

                for position in possible_positions:
                    target_row, target_col = position
                    self.make_move(row, col, target_row, target_col)
                    score = self.minimax(depth + 1, False)
                    self.undo()  # Revert the simulated move
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')  # Initialize to positive infinity
            for selection in self.get_possible_selections():
                row, col = selection
                possible_positions = self.get_possible_positions(row, col)

                for position in possible_positions:
                    target_row, target_col = position
                    self.make_move(row, col, target_row, target_col)
                    score = self.minimax(depth + 1, True)
                    self.undo()  # Revert the simulated move
                    best_score = min(score, best_score)
            return best_score
    def evaluate(self):
        score = 0
        # Static scores
        corner_score = 10
        edge_score = 5
        center_score = 15
        other_score = 3
        three_in_a_row_score = 50  # Adding a new score for three in a row

        board_size = 5

        # Evaluate static piece positions
        for row in range(board_size):
            for col in range(board_size):
                symbol = self.board.grid[row][col].symbol
                if symbol == "O" or symbol == "X":
                    # Assign score based on position type
                    position_score = 0
                    if self.is_corner_piece(row, col):
                        position_score = corner_score
                    elif row == 2 and col == 2:  # Center position
                        position_score = center_score
                    elif self.is_edge_piece(row, col):
                        position_score = edge_score
                    else:
                        position_score = other_score
                    
                    # Add or subtract the score based on the symbol
                    if symbol == self.player2.symbol:
                        score += position_score
                    else:
                        score -= position_score

        # Evaluate dynamic
        for row in range(board_size):
            for col in range(board_size - 2):  # Horizontal check
                symbols = self.board.grid[row][col:col+3]
                if all(piece.symbol == 'O' for piece in symbols):
                    score += three_in_a_row_score
                elif all(piece.symbol == 'X' for piece in symbols):
                    score -= three_in_a_row_score

        for col in range(board_size):
            for row in range(board_size - 2):  # Vertical check
                symbols = [self.board.grid[row+i][col] for i in range(3)]
                if all(piece.symbol == 'O' for piece in symbols):
                    score += three_in_a_row_score
                elif all(piece.symbol == 'X' for piece in symbols):
                    score -= three_in_a_row_score

        for index in range(board_size - 2):  # Diagonal check
            diag1_symbols = [self.board.grid[index+i][index+i] for i in range(3)]
            diag2_symbols = [self.board.grid[index+i][board_size-index-i-1] for i in range(3)]
            if all(piece.symbol == 'O' for piece in diag1_symbols) or all(piece.symbol == 'O' for piece in diag2_symbols):
                score += three_in_a_row_score
            if all(piece.symbol == 'X' for piece in diag1_symbols) or all(piece.symbol == 'X' for piece in diag2_symbols):
                score -= three_in_a_row_score

        return score



    def get_possible_selections(self):
        possible_selections = []
        for row in range(5):
            for col in range(5):
                if self.is_edge_piece(row, col) and (self.board.grid[row][col].symbol == "" or self.board.grid[row][col].symbol == "O"):
                    possible_selections.append((row, col))
        return possible_selections
