import networkx as nx
from enum import Enum, auto

# --- Enums ---
class TileType(Enum):
    FOREST = auto()
    FIELD = auto()
    MOUNTAIN = auto()
    HILL = auto()
    PASTURE = auto()
    DESERT = auto()

class NodeType(Enum):
    LAND = auto()
    BUILDING = auto()
    ROAD = auto()

class BuildingType(Enum):
    VILLAGE = auto()
    CITY = auto()

# --- Create graph ---
G = nx.Graph()

building_nodes_per_row = [3, 4, 4, 5, 5, 6, 6, 7, 7, 6, 6, 5, 5, 4, 4, 3]

G = nx.Graph()

for r, count in enumerate(building_nodes_per_row):
    for c in range(count):
        node_name = f"B-{r}-{c}"
        G.add_node(node_name, node_type="building", owner=None, building_type=None)

print(f"Total buildingsalots: {len(G.nodes)}")
print("Test some nodes:", list(G.nodes)[:80])

def print_building_nodes():
    """Prints the building nodes structure in a readable format."""
    empty_space = " " * 2
    print("Building nodes:")
    for row, column in enumerate(building_nodes_per_row):
        s_to_print = ""
        s_to_print += "____" * (7 - (column))
        for col in range(column):
            if row < 10:
                node_name = f"B-0{row}-{col}"
            else:
                node_name = f"B-{row}-{col}"
            s_to_print += f"{node_name}{empty_space}"
        print(s_to_print.strip())

# Example usage
if __name__ == "__main__":
    print_building_nodes()
    print(f"Total building nodes: {len(G.nodes)}")
    print("Graph structure:", G.edges(data=True))
