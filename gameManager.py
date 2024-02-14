class GameManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance.active_game = None
        return cls._instance

    def start_game(self, game_instance):
        if self.active_game:
            print("A game is already in progress. Cannot start a new game.")
        else:
            self.active_game = game_instance
            print("Game started.")

    def end_game(self):
        self.active_game = None
        print("Game ended.")