import math
from model.Player import Player
from controller.GameControllerAI import GameController

class AIPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
