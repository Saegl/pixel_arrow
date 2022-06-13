# pylint: disable = missing-module-docstring
from flecs import GameFramework, Config

from square_mover import config

# import gc
# gc.disable()


def main(): # pylint: disable = missing-function-docstring
    game = GameFramework(Config.from_obj_attrs(config))
    
    from square_mover.scenes.offline import Offline
    game.push(Offline(game))
    
    # from square_mover.scenes.online import Online
    # game.push(Online(game))
    
    game.gameloop()


if __name__ == "__main__":
    main()
