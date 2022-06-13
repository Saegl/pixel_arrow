import arcade
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Starting Template"

SPEED = 10.0


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.down = False
        self.up = False
        self.left = False
        self.right = False

        self.player_pos_x = 0
        self.player_pos_y = 0

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(
            self.player_pos_x, self.player_pos_y, 20.0, 20.0, arcade.color.GREEN
        )
        # self.clear()

    def on_update(self, delta_time):
        dx = dy = 0.0
        if self.up:
            # print('UP')
            dy += SPEED
        if self.down:
            # print('Down')
            dy -= SPEED
        if self.left:
            # print('Left')
            dx -= SPEED
        if self.right:
            # print("right")
            dx += SPEED

        self.player_pos_x += dx
        self.player_pos_y += dy

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.up = True
        if key == arcade.key.DOWN:
            self.down = True
        if key == arcade.key.LEFT:
            self.left = True
        if key == arcade.key.RIGHT:
            self.right = True

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.up = False
        if key == arcade.key.DOWN:
            self.down = False
        if key == arcade.key.LEFT:
            self.left = False
        if key == arcade.key.RIGHT:
            self.right = False


def main():
    """Main function"""
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
