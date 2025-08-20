import random
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
    PORT = auto()

class BuildingType(Enum):
    VILLAGE = auto()
    CITY = auto()

# --- Constants ---
FOURPLAYER_BUILDING_NODES_PER_ROW = [3, 4, 4, 5, 5, 6, 6, 5, 5, 4, 4, 3]
FOURPLAYER_LAND_NODES_PER_ROW = [3, 4, 5, 4, 3]
FOURPLAYER_LANDTILES = {TileType.FOREST: 4, TileType.FIELD: 4, TileType.MOUNTAIN: 3, TileType.HILL: 3, TileType.PASTURE: 4, TileType.DESERT: 1}
FOURPLAYER_LANDTILES_VALUES = {2: 1, 12: 1, 3: 2, 4: 2, 5: 2, 6: 2, 8: 2, 9: 2, 10: 2, 11: 2}
FOURPLAYER_PORT_POSITIONS = [
    ((0, 0), (1, 0)), 
    ((0, 1), (1, 2)), 
    ((3, 0), (4, 0)),  
    ((7, 0), (8, 0)),  
    ((10, 0), (11, 0)),  
    ((10, 2), (11, 1)),  
    ((9, 3), (8, 4)),  
    ((5, 5), (6, 5)),  
    ((3, 4), (2, 3)), 
]
FOURPLAYER_PORT_TYPES = [
    ("3:1", None),
    ("3:1", None),
    ("3:1", None),
    ("3:1", None),
    ("2:1", TileType.FOREST),
    ("2:1", TileType.FIELD),
    ("2:1", TileType.MOUNTAIN),
    ("2:1", TileType.HILL),
    ("2:1", TileType.PASTURE),
]

SIXPLAYER_BUILDING_NODES_PER_ROW = [3, 4, 4, 5, 5, 6, 6, 7, 7, 6, 6, 5, 5, 4, 4, 3]
SIXPLAYER_LAND_NODES_PER_ROW = [3, 4, 5, 6, 5, 4, 3]
SIXPLAYER_LANDTILES = {TileType.FOREST: 6, TileType.FIELD: 6, TileType.MOUNTAIN: 5, TileType.HILL: 5, TileType.PASTURE: 6, TileType.DESERT: 2}
SIXPLAYER_LANDTILES_VALUES = {2: 2, 12: 2, 3: 3, 4: 3, 5: 3, 6: 3, 8: 3, 9: 3, 10: 3, 11: 3}
SIXPLAYER_PORT_POSITIONS = [
    ((0, 0), (1, 0)), 
    ((0, 1), (1, 2)), 
    ((5, 0), (6, 0)),  
    ((8, 0), (9, 0)),  
    ((12, 0), (11, 0)),  
    ((14, 0), (15, 0)),  
    ((15, 1), (14, 2)),  
    ((13, 3), (14, 3)),  
    ((11, 4), (10, 5)),  
    ((7, 6), (8, 6)),  
    ((3, 4), (2, 3)),  
]
SIXPLAYER_PORT_TYPES = FOURPLAYER_PORT_TYPES + [
    ("3:1", None), 
    ("2:1", TileType.FIELD),
]


# --- Game Configuration ---

six_player_game = True  
if six_player_game:
    BUILDING_NODES_PER_ROW = SIXPLAYER_BUILDING_NODES_PER_ROW
    LAND_NODES_PER_ROW = SIXPLAYER_LAND_NODES_PER_ROW
    LANDTILES = SIXPLAYER_LANDTILES
    LAND_TILES_VALUES = SIXPLAYER_LANDTILES_VALUES
    PORT_POSITIONS = SIXPLAYER_PORT_POSITIONS
    PORT_TYPES = SIXPLAYER_PORT_TYPES
else:
    BUILDING_NODES_PER_ROW = FOURPLAYER_BUILDING_NODES_PER_ROW
    LAND_NODES_PER_ROW = FOURPLAYER_LAND_NODES_PER_ROW
    LANDTILES = FOURPLAYER_LANDTILES
    LAND_TILES_VALUES = FOURPLAYER_LANDTILES_VALUES
    PORT_POSITIONS = FOURPLAYER_PORT_POSITIONS
    PORT_TYPES = FOURPLAYER_PORT_TYPES

# --- Graph Initialization ---
G = nx.Graph()

def get_building_node_name(row, col):
    """Returns the standardized building node name."""
    if row < 0 or col < 0:
        raise ValueError(f"Row and column indices must be non-negative. Row: {row}, Column: {col}")
    if row >= len(BUILDING_NODES_PER_ROW) or col >= BUILDING_NODES_PER_ROW[row]:
        raise ValueError(f"Row or column index out of bounds for building nodes. Row: {row}, Column: {col}, Max Row: {len(BUILDING_NODES_PER_ROW)}, Max Column: {BUILDING_NODES_PER_ROW[row]}")
    if col < 10:
        col = f"0{col}"
    if row < 10:
        row = f"0{row}"
    return f"B-{row}-{col}"

def get_land_node_name(row, col):
    """Returns the standardized land node name."""
    if row < 0 or col < 0:
        raise ValueError(f"Row and column indices must be non-negative. Row: {row}, Column: {col}")
    if row >= len(LAND_NODES_PER_ROW) or col >= LAND_NODES_PER_ROW[row]:
        raise ValueError(f"Row or column index out of bounds for land nodes. Row: {row}, Column: {col}, Max Row: {len(LAND_NODES_PER_ROW)}, Max Column: {LAND_NODES_PER_ROW[row]}")
    return f"L-{row}-{col}"

def get_port_node_name(building_node_1, building_node_2):
    """Returns the standardized port node name."""
    if not isinstance(building_node_1, str) or not isinstance(building_node_2, str):
        raise ValueError("Building node names must be strings.")
    if building_node_1[0] != 'B' or building_node_2[0] != 'B':
        raise ValueError("Building node names must start with 'B'.")
    return f"P-{building_node_1}-{building_node_2}"

def create_building_nodes():
    for r, count in enumerate(BUILDING_NODES_PER_ROW):
        for c in range(count):
            node_name = get_building_node_name(r, c)
            G.add_node(node_name, node_type=NodeType.BUILDING, owner=None, building_type=None)


def create_land_nodes():
    all_tile_types = []
    for tile_type, count in LANDTILES.items():
        all_tile_types.extend([tile_type] * count)
    all_values = []
    for value, count in LAND_TILES_VALUES.items():
        all_values.extend([value] * count)
    random.shuffle(all_tile_types)
    random.shuffle(all_values)
    for r, count in enumerate(LAND_NODES_PER_ROW):
        for c in range(count):
            node_name = f"L-{r}-{c}"
            terrain = all_tile_types.pop()

            if terrain == TileType.DESERT:
                number = 0
            else:
                number = all_values.pop()

            G.add_node(
                node_name,
                node_type=NodeType.LAND,
                terrain=terrain,
                number=number
            )


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
                if r < len(BUILDING_NODES_PER_ROW) // 2:
                    for c in range(count):
                        node_name = get_building_node_name(r, c)
                        next_node_name_left = get_building_node_name(r + 1, c)
                        next_node_name_right = get_building_node_name(r + 1, c + 1)
                        G.add_edge(node_name, next_node_name_left, owner=None)
                        G.add_edge(node_name, next_node_name_right, owner=None)
                else:
                    for c in range(count):
                        node_name = get_building_node_name(r, c)
                        if c < count - 1:
                            next_node_name_right = get_building_node_name(r + 1, c)
                            G.add_edge(node_name, next_node_name_right, owner=None)
                        if c > 0:
                            next_node_name_left = get_building_node_name(r + 1, c - 1)
                            G.add_edge(node_name, next_node_name_left, owner=None)
                        
def create_land_edges():
    """Creates edges between land nodes and their 6 adjacent building nodes, matching the Catan board structure."""
    for r, land_count in enumerate(LAND_NODES_PER_ROW):
        for c in range(land_count):
            row_offsett = 2
            for i in range(6):
                # Calculate the coordinates of the adjacent building node
                # Top
                if i == 0:
                    building_row = r * row_offsett
                    if len(LAND_NODES_PER_ROW) // 2 < r: # If the row is in the second half of the board the column the top building node needs to be offset by 1
                        building_col = c + 1
                    else:
                        building_col = c 
                # Upper right and left
                elif i == 1:
                    building_row = r * row_offsett + 1 
                    building_col = c
                elif i == 2:
                    building_row = r * row_offsett + 1
                    building_col = c + 1
                # Bottom right and left
                elif i == 3:
                    building_row = r * row_offsett + 2
                    building_col = c
                elif i == 4:
                    building_row = r * row_offsett + 2
                    building_col = c + 1
                # Bottom
                elif i == 5:
                    building_row = r * row_offsett + 3
                    if len(LAND_NODES_PER_ROW) // 2 > r: # If the row is in the first half of the board the column the bottom building node needs to be offset by 1
                        building_col = c + 1
                    else:
                        building_col = c
                # Get the name of the building node
                building_node_name = get_building_node_name(building_row, building_col)
                # Get the name of the land node
                land_node_name = get_land_node_name(r, c)
                # Add the edge if the building node exists
                if building_node_name in G.nodes:
                    G.add_edge(land_node_name, building_node_name)

def create_ports():
    """Creates port nodes and connects them to the appropriate building nodes."""
    ports = PORT_TYPES.copy()
    random.shuffle(ports)
    for (position, (port_ratio, tile_type)) in zip(PORT_POSITIONS, ports):
        building_node_name = get_building_node_name(*position[0])
        if building_node_name not in G.nodes:
            continue
        building_node_name_2 = get_building_node_name(*position[1])
        if building_node_name_2 not in G.nodes:
            continue
        port_node_name = get_port_node_name(building_node_name, building_node_name_2)
        G.add_node(port_node_name, node_type=NodeType.PORT, ratio=port_ratio, tile_type=tile_type)
        G.add_edge(building_node_name, port_node_name, owner=None)
        G.add_edge(building_node_name_2, port_node_name, owner=None)


# --- Functions to print the graph structure --- 

def print_building_nodes():
    """Prints the building nodes structure in a readable format"""
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

def print_land_nodes(include_names=False):
    """Prints the land nodes structure in a readable format, including value and terrain."""
    empty_space = " " * 4
    print("Land nodes:")
    for row, count in enumerate(LAND_NODES_PER_ROW):
        s_to_print = ""
        if not include_names:
            s_to_print += "_____" * (7 - count)
        else:
            s_to_print += "________" * (7 - count)
        for col in range(count):
            node_name = get_land_node_name(row, col)
            if node_name in G.nodes:
                node_data = G.nodes[node_name]
                value = node_data.get("number", 0)
                value_str = f"{value:02d}"
                terrain = node_data.get("terrain", "")
                terrain_str = terrain.name[:4] if hasattr(terrain, "name") else str(terrain)[:4]
                if include_names:
                    s_to_print += f"{node_name}({value_str}{terrain_str}){empty_space}"
                else:   
                    s_to_print += f"{value_str}{terrain_str}{empty_space}"
        print(s_to_print.strip())


# Testing
if __name__ == "__main__":
    create_building_nodes()
    create_land_nodes()
    create_road_edges()
    create_land_edges()
    create_ports()
    print_building_nodes()
    print_land_nodes()
    #print(f"Total nodes: {len(G.nodes)}")
    print("Graph structure:", G.edges(data=True))
    print("Port nodes:")
    for node in G.nodes:
        if G.nodes[node].get("node_type") == NodeType.PORT:
            print(f"{node} - Ratio: {G.nodes[node].get('ratio')}, Tile Type: {G.nodes[node].get('tile_type')}")
            print(f"Connected to: {list(G.neighbors(node))}")
