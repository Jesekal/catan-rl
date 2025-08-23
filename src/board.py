from graph import setup_board, TileType, add_building, add_road, get_building_node_name, print_graph_structure, NodeType, Resource, BuildingType, TurnAction, DevelopmentCardType


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

        # Add moves for building actions
        for action in afforded_cards:
            if action == BuildingType.CITY:
                for node in self.graph.nodes:
                    if self.graph.nodes[node].get('node_type') == NodeType.BUILDING and self.graph.nodes[node].get('owner') == player_id and self.graph.nodes[node].get('building_type') == BuildingType.VILLAGE:
                        legal_moves.append((TurnAction.BUILD_CITY, node))
            elif action == BuildingType.DEVELOPMENT_CARD:
                legal_moves.append((TurnAction.BUY_DEVELOPMENT_CARD, None))
            elif action == BuildingType.ROAD:
                for edge in self.graph.edges:
                    if self.graph.edges[edge].get('owner') == player_id:
                        connected_node1 = edge[0]
                        connected_node2 = edge[1]
                        connected_nodes = [connected_node1, connected_node2]
                        for connected_node in connected_nodes:
                            for neighbor in self.graph.neighbors(connected_node):
                                if self.graph.nodes[neighbor].get('node_type') == NodeType.BUILDING:
                                    road_edge = self.graph.get_edge_data(connected_node, neighbor)
                                    if road_edge.get('owner') == 0:
                                        legal_moves.append((TurnAction.BUILD_ROAD, connected_node, neighbor))
            elif action == BuildingType.VILLAGE:
                for edge in self.graph.edges:
                    if self.graph.edges[edge].get('owner') == player_id:
                        connected_node1 = edge[0]
                        connected_node2 = edge[1]
                        connected_nodes = [connected_node1, connected_node2]
                        for connected_node in connected_nodes:
                            no_adjacent_buildings = True
                            for neighbor in self.graph.neighbors(connected_node):
                                if self.graph.nodes[neighbor].get('node_type') == NodeType.BUILDING and self.graph.nodes[neighbor].get('owner') != 0:   # Check for adjacent buildings  
                                    no_adjacent_buildings = False   
                                    break
                            if no_adjacent_buildings:
                                legal_moves.append((TurnAction.BUILD_VILLAGE, connected_node))
            
        # Add moves for playing development cards
        for development_card in self.players[player_id].get("development_cards", []):
            print(f"Player {player_id} has development card: {development_card}")
            # If development_card is a tuple like (DevelopmentCardType.KNIGHT, 0), extract the type
            card_type = development_card[0] if isinstance(development_card, tuple) else development_card
            if card_type == DevelopmentCardType.KNIGHT:
                print(f"Adding knight moves for player {player_id}")
                for node in self.graph.nodes:  # All land nodes except current and last robber position
                    if self.graph.nodes[node].get('node_type') == NodeType.LAND and node != self.robber_position and node != self.last_robber_position: 
                        legal_moves.append((TurnAction.PLAY_KNIGHT, node)) 
            elif card_type == DevelopmentCardType.ROAD_BUILDING:
                road_building_moves = []
                for edge in self.graph.edges:
                    if self.graph.edges[edge].get('owner') == player_id: # Owned by player
                        connected_node1 = edge[0]
                        connected_node2 = edge[1]
                        connected_nodes = [connected_node1, connected_node2]
                        for connected_node in connected_nodes:
                            for neighbor in self.graph.neighbors(connected_node):
                                if self.graph.nodes[neighbor].get('node_type') == NodeType.BUILDING:
                                    road_edge = self.graph.get_edge_data(connected_node, neighbor)
                                    if road_edge.get('owner') == 0:
                                        road_building_moves.append((TurnAction.PLAY_ROAD_BUILDING, connected_node, neighbor))
                # Choose second road build move
                for i in range(len(road_building_moves)):
                    grapgh_after_first_road = self.graph.copy()
                    first_road = road_building_moves[i]
                    grapgh_after_first_road.edges[(first_road[1], first_road[2])]['owner'] = player_id
                    for edge in grapgh_after_first_road.edges:
                        if grapgh_after_first_road.edges[edge].get('owner') == player_id: # Owned by player
                            connected_node1 = edge[0]
                            connected_node2 = edge[1]
                            connected_nodes = [connected_node1, connected_node2]
                            for connected_node in connected_nodes:
                                for neighbor in grapgh_after_first_road.neighbors(connected_node):
                                    if grapgh_after_first_road.nodes[neighbor].get('node_type') == NodeType.BUILDING:
                                        road_edge = grapgh_after_first_road.get_edge_data(connected_node, neighbor)
                                        if road_edge.get('owner') == 0:
                                            legal_moves.append((TurnAction.PLAY_ROAD_BUILDING, first_road[1], first_road[2], connected_node, neighbor))



                legal_moves.extend(road_building_moves)          
                # Remove duplicates
                legal_moves = list(set(legal_moves))
                
                
            # elif card_type == DevelopmentCardType.MONOPOLY:
            #     for resource in Resource:
            #         legal_moves.append((TurnAction.PLAY_MONOPOLY, resource))
            # elif card_type == DevelopmentCardType.YEAR_OF_PLENTY:
            #     for resource1 in Resource:
            #         for resource2 in Resource:
            #             legal_moves.append((TurnAction.PLAY_YEAR_OF_PLENTY, resource1, resource2))
            # elif card_type == DevelopmentCardType.VICTORY_POINT:
            #     # Victory point cards are played automatically when drawn
            #     continue

                                
        
        return legal_moves

        
        
if __name__ == "__main__":
    # Example usage
    board = Board(number_of_players=6)
    board.setup_graph()
    board.build_road(1, get_building_node_name(0,0), get_building_node_name(1,0))
    board.build_settlement(1, get_building_node_name(0,0))
    print(f"Robber is positioned at: {board.robber_position}")
    board.print_graph()
