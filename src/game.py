from board import Board
from graph import NodeType, Resource, BuildingType, get_building_node_name, DevelopmentCardType, TurnAction
import random

class Game:
    def __init__(self, number_of_players=4):
        self.number_of_players = number_of_players
        self.reset()

    def reset(self):
        """Start new game"""
        self.current_player = 1  
        self.robber_position = None
        self.dice_roll = None
        self.phase = 0
        self.round = 0

        self.players = {
            pid: {
                "resources": {r: 0 for r in Resource},
                "development_cards": [],
                "roads": 0,
                "villages": 0,
                "cities": 0,
                "victory_points": 0,
                "has_longest_road": False,
                "has_largest_army": False,
                "knights_played": 0,
            }
            for pid in range(1, self.number_of_players + 1)
        }

        self.dev_deck = (
            [DevelopmentCardType.KNIGHT] * 14
            + [DevelopmentCardType.VICTORY_POINT] * 5
            + [DevelopmentCardType.ROAD_BUILDING] * 2
            + [DevelopmentCardType.YEAR_OF_PLENTY] * 2
            + [DevelopmentCardType.MONOPOLY] * 2
        )
        random.shuffle(self.dev_deck)

        self.board = Board(self.players, cards=self.dev_deck)
        self.board.setup_graph()

        return self._get_obs()

    def step(self, action):
        """
        Kör ett drag i spelet.
        Returnerar: obs, reward, done, info
        """
        player_id = self.current_player

        # 1. Applicera draget (du får definiera logiken i Board/Game)
        self.apply_action(player_id, action)

        # 2. Reward = belöning för RL (kan vara increment i victory points)
        reward = self.players[player_id]["victory_points"]

        # 3. Kolla om spelet är klart
        done = self.is_terminal()

        # 4. Byt till nästa spelare om spelet fortsätter
        if not done:
            self.current_player = (self.current_player % self.number_of_players) + 1

        # 5. Observation + debug-info
        obs = self._get_obs()
        info = {"legal_moves": self.legal_moves(self.current_player)}

        return obs, reward, done, info

    def apply_action(self, player_id, action):
        applied_action = action[0]  # Action is a tuple, isolate TurnAction
        params = action[1:]  

        match applied_action:
            case TurnAction.BUILD_ROAD:
                self.build_road(player_id, params)

            case TurnAction.BUILD_VILLAGE:
                self.build_village(player_id, params)

            case TurnAction.BUILD_CITY:
                self.build_city(player_id, params)

            case TurnAction.BUY_DEVELOPMENT_CARD:
                self.buy_development_card(player_id)

            case TurnAction.PLAY_KNIGHT:
                self.play_knight(player_id, params)

            case TurnAction.TRADE_BANK:
                self.trade_bank(player_id, params)

            case TurnAction.END_TURN:
                self.end_turn(player_id)

            case _:
                raise ValueError(f"Unknown action: {applied_action}")
        
        self.update_board()

    def build_road(self, player_id, nodes):
        """Builds a road for selected player"""
        start_node = nodes[0]
        second_node = nodes[1]
        self.players = self.board.build_road(player_id, start_node, second_node)
        self.players[player_id]['resources'][Resource.BRICK] -= 1
        self.players[player_id]['resources'][Resource.WOOD] -= 1
        if self.players[player_id]['resources'][Resource.BRICK] < 0 or self.players[player_id]['resources'][Resource.WOOD] < 0:
            raise ValueError(f'Build road was not legal since it resulted in wood: {self.players[player_id]['resources'][Resource.WOOD]}. Brick: {self.players[player_id]['resources'][Resource.BRICK]}')

    def build_village(self, player_id, node):
        """Builds a village for player on node and update resources accordingly"""
        node = node[0]  # Isolate tuple
        self.players = self.board.build_settlement(player_id, node)
        self.players[player_id]['resources'][Resource.BRICK] -= 1
        self.players[player_id]['resources'][Resource.WOOD] -= 1
        self.players[player_id]['resources'][Resource.WHEAT] -= 1
        self.players[player_id]['resources'][Resource.SHEEP] -= 1
        if self.players[player_id]['resources'][Resource.BRICK] < 0 or self.players[player_id]['resources'][Resource.WOOD] < 0 or self.players[player_id]['resources'][Resource.SHEEP] < 0 or self.players[player_id]['resources'][Resource.WHEAT] < 0:
            raise ValueError(f'Build Village was not legal since it resulted in: {self.players[player_id]['resources']}')
                                                                                       
    def build_city(self, player_id, node):
        """Builds city for player on coordinates and update resources accordingly"""
        node = node[0]
        self.players = self.board.build_settlement(player_id, node)
        self.players[player_id]['resources'][Resource.WHEAT] -= 2
        self.players[player_id]['resources'][Resource.ORE] -= 3
        if self.players[player_id]['resources'][Resource.ORE] < 0 or self.players[player_id]['resources'][Resource.WHEAT] < 0:
            raise ValueError(f'Build city was not legal since it resulted in: {self.players[player_id]['resources']}')

    def buy_development_card(self, player_id):
        self.players[player_id]['resources'][Resource.ORE] -= 1
        self.players[player_id]['resources'][Resource.WHEAT] -= 1
        self.players[player_id]['resources'][Resource.SHEEP] -= 1
        if not self.dev_deck:
            raise ValueError("No dev cards left in the deck")
        if self.players[player_id]['resources'][Resource.ORE] < 0 or self.players[player_id]['resources'][Resource.SHEEP] < 0 or self.players[player_id]['resources'][Resource.WHEAT] < 0:
            raise ValueError(f'Buy dev-card was not legal since it resulted in: {self.players[player_id]['resources']}')
        card = self.dev_deck.pop()
        # Newly bought card is stored but usually not playable this turn
        self.players[player_id]["development_cards"].append([card, 1])      # Cards until playable (1 in catan rules)

    def end_turn(self, player_id):
        for card in self.players[player_id]["development_cards"]:
            card[1] = 0     # Set card to playable
        
        # Rotate to next player
        self.current_player = (self.current_player % self.number_of_players) + 1
        # If back to player one, next phase
        if self.current_player == 1:
            self.next_round()


    def next_round(self):
        self.round += 1
        if self.round >= 2:         # Update phase when out of initial placements
            self.phase = 1

        self.update_board() 


    def is_terminal(self):
        """Game ends when any player reaches 10 points"""
        return any(p["victory_points"] >= 10 for p in self.players.values())

    def _get_obs(self):
        """What the player ID gets to see"""
        return {
            "player_id": self.current_player,
            "resources": dict(self.players[self.current_player]["resources"]),
            "victory_points": self.players[self.current_player]["victory_points"],
            "phase": self.phase,
            "legal_moves": self.legal_moves(self.current_player),
        }

    def legal_moves(self, player_id):
        """Returns a list of legal moves for the given player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        return self.board.legal_turn_moves(player_id, self.phase)
    
    def give_resource(self, player_id, resource_type, amount):
        """Gives a specified amount of a resource to a player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        if resource_type not in self.players[player_id]["resources"]:
            raise ValueError(f"Invalid resource type: {resource_type}")
        
        self.players[player_id]["resources"][resource_type] += amount
        self.update_board()

    def set_resources(self, player_id, amoun):
        """Gives resources to a player for testing purposes."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        
        for resource in Resource:
            self.players[player_id]["resources"][resource] = amoun
        self.update_board()

    def give_development_card(self, player_id, card_type):
        """Gives a development card to a player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} does not exist.")
        if card_type not in DevelopmentCardType:
            raise ValueError(f"Invalid development card type: {card_type}")
        
        self.players[player_id]["development_cards"].append([card_type, 1]) # (card_type, turns_until_playable)  SHOULD BE 1 NORMALLY!!!
        self.update_board()

    

    def print_ports(self):
        self.board.print_ports()

    def update_board(self):
        self.board.players = self.players
        self.board.robber_position = self.robber_position
        self.board.cards = self.dev_deck

    

    

if __name__ == "__main__":
    # Example usage
    game_state = Game(number_of_players=4)
    game_state.next_round()
    game_state.next_round()
    game_state.board.build_road(1, get_building_node_name(5, 2), get_building_node_name(4, 1))
    # game_state.board.build_road(2, get_building_node_name(2, 2), get_building_node_name(1, 2))
    #game_state.set_resources(1, 1)
    # #game_state.give_development_card(2, DevelopmentCardType.KNIGHT)
    # #game_state.give_development_card(2, DevelopmentCardType.VICTORY_POINT)
    # game_state.give_development_card(2, DevelopmentCardType.VICTORY_POINT)
    # game_state.give_development_card(1, DevelopmentCardType.MONOPOLY)
    #game_state.give_development_card(2, DevelopmentCardType.YEAR_OF_PLENTY)
    game_state.give_resource(1, Resource.WOOD, 1)
    game_state.give_resource(1, Resource.BRICK, 0)
    game_state.give_resource(1, Resource.ORE, 3)
    game_state.give_resource(1, Resource.SHEEP, 1)
    game_state.give_resource(1, Resource.WHEAT, 3)
    
    # #print(f"Legal moves for player one: {game_state.legal_moves(1)}")
    # game_state.print_ports()
    print(game_state.players[game_state.current_player]['resources'])
    print(f"Legal moves for current player: {game_state.legal_moves(game_state.current_player)}")
    print(game_state.legal_moves(1)[0])
    
    game_state.apply_action(game_state.current_player, game_state.legal_moves(game_state.current_player)[0])
    
    print(game_state.players[game_state.current_player]['resources'])
    print(f"Legal moves for current player ({game_state.current_player}): {game_state.legal_moves(game_state.current_player)}")

    while True:
        game_state.apply_action(1, game_state.legal_moves(game_state.current_player)[0])
        print(f"Legal moves for current player ({game_state.current_player}): {game_state.legal_moves(game_state.current_player)}")
        if game_state.current_player == 1:
            break
        
    print(f"Legal moves for current player ({game_state.current_player}): {game_state.legal_moves(game_state.current_player)}")
    print(game_state.players[game_state.current_player]["development_cards"])
    # game_state.apply_action(1, game_state.legal_moves(1)[0])
    # print(f"Legal moves for player one: {game_state.legal_moves(1)}")
    # print(len(game_state.legal_moves(1)))

