from djinn.sprite import DrawableSprite
from djinn.game import DjinnGame
import pygame

class BeachBall(DrawableSprite):
    def __init__(self, res_store, coords):
        super(BeachBall, self).__init__(res_store, 'beachball', coords)

    def draw(self):
        self._draw()

class Playground(DjinnGame):
    def load_sprites(self):
        bb = BeachBall(self.res_store, [500, 300])
        self.assign_sprite(bb, 'beachballs', 'main')
        self.show_sprite(bb)

if __name__ == "__main__":
    game = Playground(
            [1080, 608],
            'Playground',
            'black',
            30,
            'res/')
    game.go()
