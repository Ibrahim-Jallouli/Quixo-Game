class Player:
    def __init__(self, symbol):
        # Initialize the player with a symbol (either 'X' or 'O')
        self.symbol = symbol

    def make_move(self, board, selected_row, selected_col, target_row, target_col):        
        # Check if the selected and target positions are in the same row
        if selected_row == target_row:
            self.push_row(board, selected_row, selected_col, target_col)
        else:
            self.push_column(board, selected_col, selected_row, target_row)

        board.place_piece(target_row, target_col, self)
        board.display()

    def push_row(self, board, row, selected_col, target_col):
        # Temporarily store the symbol of the selected piece
        temp_symbol = self.symbol
        # peice on the left
        if target_col == 0:
            # Move all pieces one step to the right from the selected column to the end of the row
            for col in range(selected_col, 0, -1):
                board.grid[row][col].symbol = board.grid[row][col - 1].symbol
            # Place the selected piece on the left edge of the row
            board.grid[row][0].symbol = temp_symbol
            
        # piece on the right
        elif target_col == len(board.grid[row]) - 1:
            # Move all pieces one step to the left from the selected column to the start of the row
            for col in range(selected_col, len(board.grid[row]) - 1):
                board.grid[row][col].symbol = board.grid[row][col + 1].symbol
            # Place the selected piece on the right edge of the row
            board.grid[row][-1].symbol = temp_symbol

    def push_column(self, board, col, selected_row, target_row):
        # Temporarily store the symbol of the selected piece
        temp_symbol = self.symbol

        # peice on the top
        if target_row == 0:
            # Move all pieces one step down from the selected row to the bottom of the column
            for row in range(selected_row, 0, -1):
                board.grid[row][col].symbol = board.grid[row - 1][col].symbol
            # Place the selected piece at the top of the column
            board.grid[0][col].symbol = temp_symbol
            
        # peice on the bottom
        elif target_row == len(board.grid) - 1:
            # Move all pieces one step up from the selected row to the top of the column
            for row in range(selected_row, len(board.grid) - 1):
                board.grid[row][col].symbol = board.grid[row + 1][col].symbol
            # Place the selected piece at the bottom of the column
            board.grid[-1][col].symbol = temp_symbol