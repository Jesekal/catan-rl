from board import Board
from graph import NodeType, Resource, BuildingType, get_building_node_name

class GameState:
    def __init__(self, number_of_players=4):
        self.board = None  # This will be initialized in setup_board
 
        self.current_player = 0
        self.robber_position = None
        self.dice_roll = None
        self.phase = "setup"
        self.round = 0
        self.players = {
            pid: {
            "resources": {r: 0 for r in Resource},
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
        self.board = Board(self.players, cards=None)
        self.board.setup_graph()

    def legal_moves(self, player_id):
        """Returns a list of legal moves for the given player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        return self.board.legal_turn_moves(player_id)
    
    def give_resource(self, player_id, resource_type, amount):
        """Gives a specified amount of a resource to a player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        if resource_type not in self.players[player_id]["resources"]:
            raise ValueError(f"Invalid resource type: {resource_type}")
        
        self.players[player_id]["resources"][resource_type] += amount
        self.update_board()

    def update_board(self):
        self.board.players = self.players
        self.board.robber_position = self.robber_position
        self.board.phase = self.phase
        self.board.round = self.round
        self.board.current_player = self.current_player

    

if __name__ == "__main__":
    # Example usage
    game_state = GameState(number_of_players=4)
    game_state.board.print_graph()
    game_state.board.build_settlement(1, get_building_node_name(0, 0))
    game_state.board.build_road(2, get_building_node_name(5, 2), get_building_node_name(4, 1))
    game_state.give_resource(2, Resource.WOOD, 2)
    game_state.give_resource(2, Resource.BRICK, 2)
    game_state.give_resource(1, Resource.WOOD, 2)
    game_state.give_resource(1, Resource.BRICK, 2)
    game_state.give_resource(1, Resource.ORE, 3)
    game_state.give_resource(1, Resource.SHEEP, 2)
    game_state.give_resource(1, Resource.WHEAT, 2)
    print(f"Legal moves for player one: {game_state.legal_moves(1)}")
    print(f"Legal moves for player two: {game_state.legal_moves(2)}")
    print("Game state initialized with board setup.")