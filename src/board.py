from graph import setup_board, TileType, add_building, add_road, get_building_node_name, print_graph_structure, NodeType

class Board:
    def __init__(self, number_of_players=4):
        self.number_of_players = number_of_players
        self.graph = None # This will be initialized in setup_graph
        self.robber_position = None
        self.last_robber_position = None
        self.players = {
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
    
    def setup_graph(self):
        """Initializes the graph representation of the board."""
        self.graph = setup_board(self.number_of_players)
        self.robber_position = self.get_desert_position()

    def get_desert_position(self):
        """Returns the position of the desert tile."""
        for node in self.graph.nodes:
            if self.graph.nodes[node].get('terrain') == TileType.DESERT:
                return node
        return None
    
    def build_road(self, player_id, start_node, end_node):
        """Builds a road for the given player between two nodes."""
        if player_id not in range(1, self.number_of_players + 1):
            raise ValueError(f"Player {player_id} does not exist.")
        try:
            self.graph, self.players = add_road(self.graph, self.players, player_id, start_node, end_node)
        except Exception as e:
            print(f"Failed to build road: {e}")
            raise

    def build_settlement(self, player_id, node):
        """Builds a settlement for the given player at a node."""
        if player_id not in range(1, self.number_of_players + 1):
            raise ValueError(f"Player {player_id} does not exist.")
        try:
            self.graph, self.players = add_building(self.graph, self.players, player_id, node)
        except Exception as e:
            print(f"Failed to build settlement: {e}")
            raise

    def print_graph(self):
        """Prints the current state of the graph."""
        print_graph_structure(self.graph)

    def move_robber(self, new_position):
        """Moves the robber to a new position."""
        if new_position not in self.graph.nodes:
            raise ValueError(f"Position not in graph: {new_position}")
        if new_position == self.robber_position:
            raise ValueError("Robber is already at this position.")
        if new_position == self.last_robber_position:
            raise ValueError("Cannot move robber back to the last position.")
        if new_position.get('node_type') != NodeType.LAND:
            raise ValueError("Robber can only be moved to a land node.")
        
        self.last_robber_position = self.robber_position
        self.robber_position = new_position
        print(f"Robber moved to {new_position}")
    


        
if __name__ == "__main__":
    # Example usage
    board = Board(number_of_players=6)
    board.setup_graph()
    board.build_road(1, get_building_node_name(0,0), get_building_node_name(1,0))
    board.build_settlement(1, get_building_node_name(0,0))
    print(f"Robber is positioned at: {board.robber_position}")
    board.print_graph()
