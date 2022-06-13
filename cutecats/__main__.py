from flecs import GameFramework, Config
from cutecats import config


def main():
    flecs_config = Config.from_obj_attrs(config)
    game = GameFramework(flecs_config)

    # from cutecats.scenes.fight import FightScene
    # game.push(FightScene(game))

    from cutecats.scenes.start import StartScene
    game.push(StartScene(game))

    # from cutecats.scenes.multiplayer_chooser import MultiplayerChooser
    # game.push(MultiplayerChooser(game))

    # from cutecats.scenes.new_server_dialog import NewServerDialog
    # game.push(NewServerDialog(game))

    game.gameloop()


if __name__ == "__main__":
    main()
