import random
from game import Game

if __name__ == "__main__":
    game = Game(number_of_players=4)

    done = False
    obs = game._get_obs()

    while not done:
        player = game.current_player
        legal = game.legal_moves(player)

        if not legal:
            print(f"Player {player} has no legal moves.")
            break

        # Välj ett slumpmässigt drag
        action = random.choice(legal)
        print(f"\nPlayer {player} gör drag: {action}")

        obs, reward, done, info = game.step(action)

        # Debugutskrifter
        print(f"Reward för Player {player}: {reward}")
        print(f"Nästa spelare: {game.current_player}")
        #print(f"Antal möjliga drag nästa tur: {len(info['legal_moves'])}")

    print("\n========= GAME OVER =========")
    for pid, pdata in game.players.items():
        print(f"Player {pid} VPs: {pdata['victory_points']} | Resources: {pdata['resources']}")