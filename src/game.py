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
print("Test som nodes:", list(G.nodes)[:80])
