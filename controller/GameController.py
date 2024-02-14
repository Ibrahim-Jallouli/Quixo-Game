# quixo/Controller/game_controller.py
from model.QuixoBoard import QuixoBoard
from model.Player import Player

class GameController:
    def __init__(self):
        self.board = QuixoBoard()
        self.player1 = Player("X")
        self.player2 = Player("O")
        self.current_player = self.player1
        self.history = []

    def switch_player(self):
    # Switch the current player for the next turn
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def make_move(self, rowS, colS, rowT, colT):
        # save the board state before the move
        self.save_history() 
        self.current_player.make_move(self.board, rowS, colS, rowT, colT) 
        self.switch_player()
        

    def get_possible_positions(self, row, col):
        possible_positions = []

        # Check if it's a corner piece so two possible positions
        if self.is_corner_piece(row, col):
            # Check the edges of the same row
            for c in [0, 4]:
                if c != col:
                    possible_positions.append((row, c))

            # Check the edges of the same column
            for r in [0, 4]:
                if r != row:
                    possible_positions.append((r, col))
        else: # Not a corner piece 3 possible positions
            # Check the edges of the same row
            if col == 0 or col == 4:
                possible_positions.append((row, 0 if col == 4 else 4))
            else:
                possible_positions.append((row, 0))
                possible_positions.append((row, 4))

            # Check the edges of the same column
            if row == 0 or row == 4:
                possible_positions.append((0 if row == 4 else 4, col))
            else:
                possible_positions.append((0, col))
                possible_positions.append((4, col))

        return possible_positions
    
    def is_corner_piece(self, row, col):
        return (row == 0 or row == 4) and (col == 0 or col == 4)

    def is_edge_piece(self, row, col):
        return row == 0 or row == 4 or col == 0 or col == 4

    def is_empty_piece(self, row, col):
        return self.board.grid[row][col].symbol == ""
    
    def can_rechoose_piece(self, row, col):
        if(self.current_player.symbol == self.board.grid[row][col].symbol):
            return True

    def is_game_over(self):
        board = self.board.grid
        symbols = ['X', 'O']
        # Check rows and columns
        for symbol in symbols:
            for i in range(5):
                row_win = all(board[i][j].symbol == symbol for j in range(5))
                col_win = all(board[j][i].symbol == symbol for j in range(5))
                if row_win:
                    return True, symbol, ('row', i)
                if col_win:
                    return True, symbol, ('col', i)
        # Check diagonals
                diag1_win = all(board[i][i].symbol == symbol for i in range(5))
                diag2_win = all(board[i][4 - i].symbol == symbol for i in range(5))
                if diag1_win:
                    return True, symbol, ('diag', 1)
                if diag2_win:
                    return True, symbol, ('diag', 2)

        return False, None, None  # No win condition met
    
    def get_board_state(self):
        board_state = []
        for row in self.board.grid:
            board_row = []
            for piece in row:
                board_row.append(piece.symbol)
            board_state.append(board_row)
        return board_state
    
    def save_history(self):
        memento = self.board.save_state()
        self.history.append(memento)
    
    def undo(self):
        # Check if there is any state to undo
        if len(self.history) > 0:
            # Retrieve the last state without removing it
            last_state = self.history[-1]
            self.board.restore_state(last_state)
            # Now remove the last item from the list
            self.history.pop()
            # Switch the player back to who it was before the last move
            self.switch_player()
        
            return True
        else:
            # If there's nothing to undo inform the caller
            return False

