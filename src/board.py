from graph import setup_board, TileType, add_building, add_road, get_building_node_name, print_graph_structure, NodeType, Resource, BuildingType


class Board:
    def __init__(self, players, cards=None):
        self.graph = None # This will be initialized in setup_graph
        self.robber_position = None
        self.last_robber_position = None
        self.players = players  # A dictionary mapping player IDs to their data
        self.number_of_players = len(players)
        self.buying_actions = { 
            BuildingType.ROAD: {Resource.WOOD: 1, Resource.BRICK: 1},
            BuildingType.VILLAGE: {Resource.WOOD: 1, Resource.BRICK: 1, Resource.SHEEP: 1, Resource.WHEAT: 1},
            BuildingType.CITY: {Resource.ORE: 3, Resource.WHEAT: 2},
            BuildingType.DEVELOPMENT_CARD: {Resource.ORE: 1, Resource.WHEAT: 1, Resource.SHEEP: 1},
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

    def afforded_turn_moves(self, player_id):
        """Returns a list of afforded moves for the given player during their turn."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")

        player_resources = self.players[player_id].get("resources", {})
        moves = []

        for action, cost in self.buying_actions.items():
            affordable = True
            for resource, amount in cost.items():
                if player_resources.get(resource, 0) < amount:
                    affordable = False
                    break
            if affordable:
                moves.append(action)


        return moves
    
    def legal_turn_moves(self, player_id):
        """Returns a list of legal moves for the given player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        afforded_cards = self.afforded_turn_moves(player_id)
        
        legal_moves = []
        for action in afforded_cards:
            if action == BuildingType.CITY:
                for node in self.graph.nodes:
                    if self.graph.nodes[node].get('node_type') == NodeType.BUILDING and self.graph.nodes[node].get('owner') == player_id and self.graph.nodes[node].get('building_type') == BuildingType.VILLAGE:
                        legal_moves.append((action, node))
            elif action == BuildingType.DEVELOPMENT_CARD:
                legal_moves.append((action, None))
        
        return legal_moves

        
        
if __name__ == "__main__":
    # Example usage
    board = Board(number_of_players=6)
    board.setup_graph()
    board.build_road(1, get_building_node_name(0,0), get_building_node_name(1,0))
    board.build_settlement(1, get_building_node_name(0,0))
    print(f"Robber is positioned at: {board.robber_position}")
    board.print_graph()
