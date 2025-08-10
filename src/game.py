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
land_nodes_per_row = [3, 4, 5, 6, 5, 4, 3, 2]

G = nx.Graph()

# Create building nodes
def create_building_nodes():
    for r, count in enumerate(building_nodes_per_row):
        for c in range(count):
            node_name = f"B-{r}-{c}"
            G.add_node(node_name, node_type=NodeType.BUILDING, owner=None, building_type=None)

# Create land nodes
def create_land_nodes():
    for r, count in enumerate(land_nodes_per_row):
        for c in range(count):
            node_name = f"L-{r}-{c}"
            G.add_node(node_name, node_type=NodeType.LAND, owner=None, building_type=None)

# Create road nodes
def create_road_nodes():
    for r in range(len(building_nodes_per_row) - 1):
        for c in range(min(building_nodes_per_row[r], building_nodes_per_row[r + 1])):
            road_node_name = f"R-{r}-{c}"
            G.add_node(road_node_name, node_type=NodeType.ROAD, owner=None)


def print_building_nodes():
    """Prints the building nodes structure in a readable format using actual nodes."""
    empty_space = " " * 2
    print("Building nodes:")
    for row, count in enumerate(building_nodes_per_row):
        s_to_print = ""
        s_to_print += "____" * (7 - count)
        for col in range(count):
            node_name = f"B-{row}-{col}"
            if node_name in G.nodes:
                if row < 10:
                    node_name = f"B-0{row}-{col}"
                s_to_print += f"{node_name}{empty_space}"
        print(s_to_print.strip())

def print_land_nodes():
    """Prints the land nodes structure in a readable format using actual nodes."""
    empty_space = " " * 2
    print("Land nodes:")
    for row, count in enumerate(land_nodes_per_row):
        s_to_print = ""
        s_to_print += "____" * (7 - count)
        for col in range(count):
            node_name = f"L-{row}-{col}"
            if node_name in G.nodes:
                s_to_print += f"{node_name}{empty_space}"
        print(s_to_print.strip())

# Example usage
if __name__ == "__main__":
    create_building_nodes()
    create_land_nodes()
    #create_road_nodes()
    print_building_nodes()
    print_land_nodes()
    print(f"Total nodes: {len(G.nodes)}")
    print("Graph structure:", G.edges(data=True))
