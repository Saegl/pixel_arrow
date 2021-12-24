class DrawMixin:
    def setup_draw(self, image_store, screen) -> None:
        self.image_store = image_store
        self.screen = screen

    def draw(self):
        raise Exception("Abstract")


class UpdateMixin:
    def setup_update(self, game):
        self.game = game

    def update(self):
        raise Exception("Abstract")
