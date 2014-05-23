from djinn.sprite import BitmapSprite, DjinnGroup
from djinn.game import DjinnGame
from djinn.utils import Colours
from djinn.io import DjinnKeyboard
from djinn.animation import DjinnAnimation
import pygame

class BeachBall(DjinnSprite):
    def __init__(self, res):
        super(BeachBall, self).__init__('res/beachball.dj')
        self.set_frame('beachball')
        #self.set_animation(DjinnAnimation('spin', range(9)))

    def draw(self):
        if self._draw_w_animate():
            self.animation.set_active(False)

class Playground(DjinnKeyboard, DjinnGame):
    def load_sprites(self):
        self.register_group('beachballs')

        bb = BeachBall(self.res)
        self.assign_sprite(bb, 'beachballs', 'main')
        self.show_sprite(bb)

    def register_keys(self):
        def f(self, spr):
            spr.animation.set_active(True)

        ball = self.get_sprite('beachballs', 'main')
        self._register(pygame.K_SPACE, f, ball)

if __name__ == "__main__":
    game = Playground(
            [100, 100],
            'Playground',
            Colours.white,
            30,
            'res/ball.dj')
    game.go()
