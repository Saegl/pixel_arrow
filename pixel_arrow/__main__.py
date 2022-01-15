import pygame as pg
from flecs import GameFramework, Config
from flecs.image_store import fast_load_alpha, scale_nx
from pixel_arrow import config


def preprocess_images(game: GameFramework):
    store = game.res.images
    # TODO move this function from __main__ to somewhere else

    keys = "0123456789abcdefghijklmnopqrstuvwxyz"
    # TODO don't store dict in ImageStore
    store.tiles = {}
    for i in range(1, len(keys)):
        # TODO Remove hardcoded path
        tile_image = fast_load_alpha(
            f"pixel_arrow/res/images/Tiles/Tile-{str(i).zfill(2)}.png"
        )
        tile_image = scale_nx(tile_image, 2)
        store.tiles[keys[i]] = tile_image

    store.background = pg.transform.scale(store.background, config.screen_size)

    store.menu_popup = scale_nx(store.menu_popup, 5)
    store.menu_button_default = scale_nx(store.menu_button_default, 5)
    store.menu_button_active = scale_nx(store.menu_button_active, 5)
    store.heart = scale_nx(store.heart, 3)
    store.tiles_list = scale_nx(store.tiles_list, 2)


def main():
    flecs_config = Config.from_obj_attrs(config)
    game = GameFramework(flecs_config)
    preprocess_images(game)

    # from pixel_arrow.scenes.empty import EmptyScene
    # game.push(EmptyScene(game))

    # from pixel_arrow.scenes.singleplayer import SingleplayerScene
    # game.push(SingleplayerScene(game))

    from pixel_arrow.scenes.menu import MenuScene

    game.push(MenuScene(game))

    # from pixel_arrow.scenes.level_editor import LevelEditorScene
    # game.push(LevelEditorScene(game))

    game.gameloop()


if __name__ == "__main__":
    main()
