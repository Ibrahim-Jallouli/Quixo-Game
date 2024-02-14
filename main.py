from controller.GameController import GameController
from controller.GameControllerAI import GameControllerAI
from view.QuixoGUI import QuixoGUI
from gameManager import GameManager
import tkinter as tk

game_manager = GameManager()

def start_game(mode):
    if game_manager.active_game:
        print("A game is already in progress. Cannot start a new game.")
        return

    if mode == "Human vs Human":
        game_controller = GameController()
    elif mode == "Human vs AI":
        game_controller = GameControllerAI()

    if not game_manager.active_game:  # Check again after starting the game
        game_manager.start_game(game_controller)
        root = tk.Tk()
        quixo_gui = QuixoGUI(root, game_manager,game_controller)
        quixo_gui.run()
   

def show_welcome_window():
    # This function creates a welcome window with two buttons to select the game mode
    welcome_window = tk.Tk()
    welcome_window.title("Welcome to Quixo")
    label = tk.Label(text="QUIXO GAME" ,font=('Helvetica', 16),pady=20,padx=70)
    label.grid(row=0, column=0)
    # Button for human vs. human mode
    btn_human_vs_human = tk.Button(welcome_window, text="Human vs Human",
                                   command=lambda: [ start_game("Human vs Human")],#welcome_window.destroy(),
                                   width=20)
    btn_human_vs_human.grid(padx=20, pady=20)

    # Button for human vs. AI mode
    btn_human_vs_ai = tk.Button(welcome_window, text="Human vs AI",
                                command=lambda: [start_game("Human vs AI")],#welcome_window.destroy(),
                                width=20)
    btn_human_vs_ai.grid(padx=20, pady=20)

    welcome_window.mainloop()

if __name__ == "__main__":
    show_welcome_window()