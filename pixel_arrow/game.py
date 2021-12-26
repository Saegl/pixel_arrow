from pixel_arrow.framework import GameFramework
from pixel_arrow.multiplayer_scene import MultiplayerScene
from pixel_arrow.menu_scene import MenuScene

def main():
    game = GameFramework()
    game.push(MultiplayerScene(game))
    # game.push(MenuScene(game))
    game.gameloop()


if __name__ == "__main__":
    main()
