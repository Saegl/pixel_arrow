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


def cell_to_rect(x, y, tile_size):
    return pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)


def grid_loc_point(point: pg.math.Vector2) -> pg.math.Vector2:
    return pg.math.Vector2(point.x // 48, point.y // 48)


def grid_loc_box(rect: pg.Rect) -> pg.math.Vector2:
    return grid_loc_point(pg.math.Vector2(rect.centerx, rect.centery))


def collide(collision: Collision, dv: pg.math.Vector2) -> bool:
    collision.box.x += dv.x
    collision.box.y += dv.y
    loc = grid_loc_box(collision.box)

    tiles_loc = [
        pg.math.Vector2(loc.x + 1, loc.y + 1),  # bottom right
        pg.math.Vector2(loc.x + 0, loc.y + 1),  # bottom
        pg.math.Vector2(loc.x - 1, loc.y + 1),  # bottom left
        pg.math.Vector2(loc.x + 1, loc.y - 1),  # top right
        pg.math.Vector2(loc.x + 0, loc.y - 1),  # top
        pg.math.Vector2(loc.x - 1, loc.y - 1),  # top left
        pg.math.Vector2(loc.x + 1, loc.y),  # right
        pg.math.Vector2(loc.x - 1, loc.y),  # left
    ]

    # TODO remove Vector2
    collisions = filter(
        lambda loc: collision.tiles[int(loc.x)][int(loc.y)] != "0", tiles_loc
    )
    collisions = map(lambda loc: cell_to_rect(loc.x, loc.y, 48), collisions)

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
