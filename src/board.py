from graph import setup_board, TileType

class Board:
    def __init__(self, number_of_players=4):
        self.number_of_players = number_of_players
        self.graph = None # This will be initialized in setup_graph
        self.robber_position = None
    
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
    

if __name__ == "__main__":
    # Example usage
    board = Board(number_of_players=4)
    board.setup_graph()
    print(f"Robber is positioned at: {board.robber_position}")
    print(f"Graph nodes: {list(board.graph.nodes)}")