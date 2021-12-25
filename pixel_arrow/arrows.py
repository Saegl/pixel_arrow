from dataclasses import dataclass
from enum import Enum

from pygame import Rect, Surface


from pixel_arrow.gamemap import Map
from pixel_arrow.vector import Vector2D
from pixel_arrow.mixins import DrawMixin, UpdateMixin


ARROW_SPEED = 15.0


class ArrowState(Enum):
    fly = 0
    stuck = 1
    dissapear = 2


@dataclass
class Arrow:
    pos: Vector2D
    left: bool
    state: ArrowState
    frames: int = 0

    def get_image(self, image_store):
        if self.state == ArrowState.stuck:
            duration = 4
            n = self.frames // duration
            images = image_store.arrow_stuck[not self.left]
            if n >= len(images):
                return images[-1]
            return images[n]
        if self.left:
            return image_store.arrow_left
        return image_store.arrow

    def damagebox(self) -> Rect:
        return Rect(self.pos.x, self.pos.y + 12, 36, 12)

    def on_screen(self, screen: Surface):
        screenbox = screen.get_rect()
        arrowbox = self.damagebox()
        return not (arrowbox.right < screenbox.left or arrowbox.left > screenbox.right)

    def collide(self, map_: Map) -> bool:
        damagebox = self.damagebox()
        arrow_head = damagebox.left if self.left else damagebox.right
        grid_loc: Vector2D = map_.grid_loc(Vector2D(arrow_head, damagebox.centery))
        tile_type = map_.tile_type(grid_loc)
        if tile_type == "0":
            return False
        tile_rect = map_.cell_to_rect(grid_loc)
        return damagebox.colliderect(tile_rect)

    def collide_x(self, dx: float, map_: Map):
        ans = self.collide(map_)
        return ans

    def collide_player(self, player):
        damagebox = self.damagebox()
        playerbox = player.rect
        return damagebox.colliderect(playerbox)

    def damage(self, player):
        player.get_damage(1)
        self.state = ArrowState.dissapear


class Arrows(DrawMixin, UpdateMixin):
    def __init__(self, image_store, screen, game) -> None:
        self.setup_draw(image_store, screen)
        self.setup_update(game)

        self.arrows: list[Arrow] = []

    def launch_an_arrow(self, arrow: Arrow):
        self.arrows.append(arrow)

    def update(self):
        player = self.game.player
        arrows_on_screen = []
        for arrow in self.arrows:
            if arrow.state == ArrowState.fly:
                dx = -ARROW_SPEED if arrow.left else ARROW_SPEED
                arrow.pos.x += dx
                for opponent in self.game.opponents:
                    if arrow.collide_player(opponent):
                        arrow.damage(opponent)
                if arrow.collide_player(player):
                    arrow.damage(player)

                elif arrow.collide_x(dx, self.game.map):
                    arrow.state = ArrowState.stuck
            elif arrow.state == ArrowState.stuck:
                arrow.frames += 1
            elif arrow.state == ArrowState.dissapear:
                continue
            arrows_on_screen.append(arrow)

        arrows_on_screen = list(
            filter(lambda a: a.on_screen(self.screen), arrows_on_screen)
        )
        self.arrows = arrows_on_screen

    def draw(self):
        screen = self.screen
        for arrow in self.arrows:
            # pg.draw.rect(screen, (200, 100, 100), arrow.damagebox())
            screen.blit(arrow.get_image(self.image_store), arrow.pos.xy)
