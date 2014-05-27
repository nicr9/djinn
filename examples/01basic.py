from djinn.sprite import DjinnSprite, DjinnGroup
from djinn.game import DjinnGame
from djinn.utils import Colours
from djinn.io import DjinnKeyboard
from djinn.animation import DjinnAnimation
import pygame

class BeachBall(DjinnSprite):
    def __init__(self, res_store):
        super(BeachBall, self).__init__(res_store, 'beachball')
        self.set_frame('beachball')

    def draw(self):
        pass

class Playground(DjinnGame):
    def load_sprites(self):
        bb = BeachBall(self.res_store)
        self.assign_sprite(bb, 'beachballs', 'main')
        self.show_sprite(bb)

if __name__ == "__main__":
    game = Playground(
            [100, 100],
            'Playground',
            'black',
            30,
            'res/')
    game.go()
