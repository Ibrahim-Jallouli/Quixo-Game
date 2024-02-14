import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font as font
from controller.GameController import GameController
from controller.GameControllerAI import GameControllerAI
from model.AIPlayer import AIPlayer

class QuixoGUI:
    def __init__(self, root,game_manager,game_controller):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.root.title("Quixo Game")
        self.game_manager = game_manager

        # Depending on our selected game mode, retrieve the game controller from the main
        self.game_controller=game_controller

        self.playerTurn ="Player 1"
        board_size = 5
        # tres important pour la logique du jeu ( None va retourner false dans un if) 
        # si non elle va recuperer la position de la piece selectionnee (row col)
        self.selected_piece = None  
        self.is_choosing = False

        # ----------------------Design----------------------
        myFont = font.Font(weight="bold")
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move,width=10)
        self.undo_button.grid(row=7, columnspan=board_size, pady=15)
        if isinstance(self.game_controller, GameControllerAI):
            turn_label_text = "Your Turn"
        else:
            turn_label_text = f"{self.playerTurn}'s Turn"
        
        self.turn_label = tk.Label(self.root, text=turn_label_text, font=('Helvetica', 16))
        print("turn_label_text : ",turn_label_text)
        self.turn_label.grid(row=0, column=0, columnspan=board_size)
        # --------------------------------------------------

        # creer l'interface graphique
        self.buttons = [[None for _ in range(board_size)] for _ in range(board_size)]
        for i in range(board_size):
            for j in range(board_size):
                button = tk.Button(root, text="", width=5, height=2, 
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button['font'] = myFont

                button.grid(row=i+1, column=j)
                # Check if the button is an edge 
                if i in [0, board_size - 1] or j in [0, board_size - 1]:
                    # It's an edge piece, so we leave it enabled
                    self.buttons[i][j] = button
                else:
                    # It's not an edge piece, so disable it
                    button.config(state=tk.DISABLED)
                    self.buttons[i][j] = button
        self.update_display()

    def update_display(self):
        board_state = self.game_controller.get_board_state()
        if not isinstance(self.game_controller, GameControllerAI):
            self.turn_label.config(text=f"{self.playerTurn}'s Turn")
        for i in range(5):
            for j in range(5):
                piece = board_state[i][j]
                self.buttons[i][j].config(text=piece, bg="SystemButtonFace")

    # fonction appelee lorsqu'un bouton est clique deux evenements possibles
    def on_button_click(self, row, col):        
        if not self.is_choosing:
            self.select_piece(row, col)
        else:
            self.choose_position(row, col)
            if isinstance(self.game_controller.current_player, AIPlayer):
                ai_move = self.game_controller.get_ai_move()
                print("AI BEST MOVE : ",ai_move)
                self.game_controller.make_move(*ai_move)
                self.update_display()
                self.check_game_over()

    def select_piece(self, row, col):
        is_edge = self.game_controller.is_edge_piece(row, col)
        is_empty = self.game_controller.is_empty_piece(row, col)
        can_rechoose = self.game_controller.can_rechoose_piece(row, col)
        if is_edge and (is_empty or can_rechoose):
            self.undo_button.config(state=tk.DISABLED)
            self.buttons[row][col].config(bg="#23798E")
            self.highlight_valid_positions(row, col)
            self.is_choosing = True
            self.selected_piece = (row, col)
        else:
            messagebox.showinfo("Invalid Move", "Choose a valid edge piece.")


    def highlight_valid_positions(self, row, col):
        for pos in self.game_controller.get_possible_positions(row, col):    # pos est un tuple (row, col)
            self.buttons[pos[0]][pos[1]].config(bg="#C60030")

    def choose_position(self, row, col):
        position = (row, col)  # creation d'un variable position qui va contenir le (row, col ) choisi
        if position in self.game_controller.get_possible_positions(self.selected_piece[0], self.selected_piece[1]):
            #print("possible positions : ",self.game_controller.get_possible_positions(self.selected_piece[0], self.selected_piece[1]))
            #print("position : ",position)
            self.game_controller.make_move(self.selected_piece[0], self.selected_piece[1],row,col)
            self.playerTurn = "Player 2" if self.playerTurn == "Player 1" else "Player 1"
            self.update_display()
            self.is_choosing = False
            self.selected_piece = None
            self.clear_highlights()
            self.undo_button.config(state=tk.NORMAL)
            game_over, winner, winning_line = self.game_controller.is_game_over()
            if game_over:
                self.highlight_winner(winning_line)
                winner_name = "Player 1" if winner == "X" else "Player 2"
                messagebox.showinfo("Game Over", f"{winner_name} wins!")
        else:
            messagebox.showinfo("Invalid Move", "Please choose a valid position.")

    def highlight_winner(self, winning_line):
        win_type, index = winning_line
        if win_type == 'row':
            for j in range(5):
                self.buttons[index][j].config(bg="green")  # Change to winning color
        elif win_type == 'col':
            for i in range(5):
                self.buttons[i][index].config(bg="green")  # Change to winning color
        elif win_type == 'diag':
            if index == 1:
                for i in range(5):
                    self.buttons[i][i].config(bg="green")  # Change to winning color
            elif index == 2:
                for i in range(5):
                    self.buttons[i][4 - i].config(bg="green")  # Change to winning color
                    
    def clear_highlights(self):
        for row in self.buttons:
            for button in row:
                button.config(bg="SystemButtonFace")

    def undo_move(self):
        if self.game_controller.undo():
            self.playerTurn = "Player 2" if self.playerTurn == "Player 1" else "Player 1"
            self.update_display()  # Refreshes the board display
            if isinstance(self.game_controller, GameControllerAI):
                self.game_controller.undo()
                self.update_display()
            self.clear_highlights()  
        else:
            messagebox.showinfo("Undo", "No moves to undo!")
    def check_game_over(self):
        game_over, winner, winning_line = self.game_controller.is_game_over()
        if game_over:
            self.end_game(winner, winning_line)
            
    def end_game(self, winner, winning_line):
        self.highlight_winner(winning_line)
        winner_name = "Player 1" if winner == "X" else "AI"
        messagebox.showinfo("Game Over", f"{winner_name} wins!")
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)  # Disable all buttons after game ends           

    def run(self):
        self.root.mainloop()

    def on_window_close(self):
        # Update GameManager when the window is closed
        self.game_manager.end_game()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = QuixoGUI(root)
    gui.run()

