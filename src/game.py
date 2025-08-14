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

class BuildingType(Enum):
    VILLAGE = auto()
    CITY = auto()

# --- Create graph ---
G = nx.Graph()

BUILDING_NODES_PER_ROW = [3, 4, 4, 5, 5, 6, 6, 7, 7, 6, 6, 5, 5, 4, 4, 3]
LAND_NODES_PER_ROW = [3, 4, 5, 6, 5, 4, 3, 2]

G = nx.Graph()

def get_building_node_name(row, col):
    """Returns the standardized building node name."""
    return f"B-{row}-{col}"

def get_land_node_name(row, col):
    """Returns the standardized land node name."""
    return f"L-{row}-{col}"

def create_building_nodes():
    for r, count in enumerate(BUILDING_NODES_PER_ROW):
        for c in range(count):
            node_name = get_building_node_name(r, c)
            G.add_node(node_name, node_type=NodeType.BUILDING, owner=None, building_type=None)


def create_land_nodes():
    for r, count in enumerate(LAND_NODES_PER_ROW):
        for c in range(count):
            node_name = f"L-{r}-{c}"
            G.add_node(node_name, node_type=NodeType.LAND, owner=None, building_type=None)


def create_road_edges():
    """Creates edges between building nodes to represent roads."""
    for r, count in enumerate(BUILDING_NODES_PER_ROW):
        if r != len(BUILDING_NODES_PER_ROW) - 1:    # Last row does not connect to any row below it
            # Odd value on r means that the nodes on current row will connect straight down to the next row
            if r % 2:
                for c in range(count):
                    node_name = get_building_node_name(r, c)
                    next_node_name = get_building_node_name(r + 1, c)
                    G.add_edge(node_name, next_node_name, owner=None)
            else:
                # First half of even-value-rows will always connenct to two nodes on the next row
                if r < len(BUILDING_NODES_PER_ROW):
                    for c in range(count):
                        node_name = get_building_node_name(r, c)
                        next_node_name_left = get_building_node_name(r + 1, c)
                        next_node_name_right = get_building_node_name(r + 1, c + 1)
                        G.add_edge(node_name, next_node_name_left, owner=None)
                        G.add_edge(node_name, next_node_name_right, owner=None)
                else:
                    for c in range(count):
                        node_name = f"B-{r}-{c}"
                        if c < count - 1:
                            next_node_name_right = get_building_node_name(r + 1, c)
                            G.add_edge(node_name, next_node_name_right, owner=None)
                        if c > 0:
                            next_node_name_left = get_building_node_name(r + 1, c + 1)
                            G.add_edge(node_name, next_node_name_left, owner=None)
                        



                

def print_building_nodes():
    """Prints the building nodes structure in a readable format using actual nodes."""
    empty_space = " " * 2
    print("Building nodes:")
    for row, count in enumerate(BUILDING_NODES_PER_ROW):
        s_to_print = ""
        s_to_print += "____" * (7 - count)
        for col in range(count):
            node_name = get_building_node_name(row, col)
            if node_name in G.nodes:
                s_to_print += f"{node_name}{empty_space}"
        print(s_to_print.strip())

def print_land_nodes():
    """Prints the land nodes structure in a readable format using actual nodes."""
    empty_space = " " * 2
    print("Land nodes:")
    for row, count in enumerate(LAND_NODES_PER_ROW):
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
    create_road_edges()
    print_building_nodes()
    #print_land_nodes()
    #print(f"Total nodes: {len(G.nodes)}")
    print("Graph structure:", G.edges(data=True))
