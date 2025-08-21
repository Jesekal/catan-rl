class GameState:
    def __init__(self, number_of_players=4):
        self.board = None  # This will be initialized in setup_board
        self.current_player = 0
        self.robber_position = None
        self.dice_roll = None
        self.phase = "setup"
        self.round = 0

        players = {
        pid: {
            "resources": {r: 0 for r in ["wood", "brick", "sheep", "wheat", "ore"]},  
            "development_cards": [],
            "roads": 0,
            "villages": 0,
            "cities": 0,
            "victory_points": 0,
            "dev_cards": [],
            "has_longest_road": False,
            "has_largest_army": False,
        }
        for pid in range(1, number_of_players + 1)
}

        

    def legal_moves(self, player_id):
        """Returns a list of legal moves for the given player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        moves = []
        
        
        return moves