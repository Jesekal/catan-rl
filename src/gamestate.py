class GameState:
    def __init__(self, number_of_players=4):
        self.board = None  # This will be initialized in setup_board
        self.current_player = 0
        self.robber_position = None
        self.dice_roll = None
        self.phase = "setup"
        self.round = 0


    def legal_moves(self, player_id):
        """Returns a list of legal moves for the given player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        moves = []
        
        
        return moves