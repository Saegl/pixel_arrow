import pygame as pg
from flecs import System, Scene

from pixel_arrow.components.collision import Collision
from pixel_arrow.components.position import Position


class CollisionBoxUpdate(System):
    def process(self, _, scene: Scene):
        for _, (pos, collision) in scene.get_entities(Position, Collision):
            pos: Position
            collision: Collision

            collision.box.x = pos.v.x + collision.offset.x
            collision.box.y = pos.v.y + collision.offset.y


def collide_with(collider: pg.Rect, collisions: list[pg.Rect]) -> bool:
    return any([collider.colliderect(x) for x in collisions])


def cell_to_rect(x, y, tile_size) -> pg.Rect:
    return pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)


def grid_loc_point(point_x: int, point_y: int) -> tuple[int, int]:
    return point_x // 48, point_y // 48


def grid_loc_box(rect: pg.Rect) -> tuple[int, int]:
    return grid_loc_point(rect.centerx, rect.centery)


def collide(collision: Collision, dv: pg.math.Vector2) -> bool:
    collision.box.x += dv.x
    collision.box.y += dv.y
    loc = grid_loc_box(collision.box)

    tiles_loc = [
        (loc[0] + 1, loc[1] + 1),  # bottom right
        (loc[0] + 0, loc[1] + 1),  # bottom
        (loc[0] - 1, loc[1] + 1),  # bottom left
        (loc[0] + 1, loc[1] - 1),  # top right
        (loc[0] + 0, loc[1] - 1),  # top
        (loc[0] - 1, loc[1] - 1),  # top left
        (loc[0] + 1, loc[1]),  # right
        (loc[0] - 1, loc[1]),  # left
    ]

    collisions = filter(
        lambda loc: collision.tiles[loc[0]][loc[1]] != "0", tiles_loc
    )
    collisions = map(lambda loc: cell_to_rect(loc[0], loc[1], 48), collisions)

    ans = collide_with(collision.box, list(collisions))

    collision.box.x -= dv.x
    collision.box.y -= dv.y
    return ans


def collide_y(collision: Collision, dy) -> bool:
    return collide(collision, pg.math.Vector2(0.0, dy))


def collide_x(collision: Collision, dx) -> bool:
    return collide(collision, pg.math.Vector2(dx, 0.0))


def on_ground(collision: Collision) -> bool:
    return collide_y(collision, 1.0)
