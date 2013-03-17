from utils import mul_lists, add_lists, sub_lists
from os.path import isfile
import pygame

class DjinnSprite(pygame.sprite.Sprite):
    def __init__(self, res, res_name, coords, size=[16, 16]):
        super(DjinnSprite, self).__init__()

        self.screen = res.screen
        self.res = res
        self.res_name = res_name

        self.size = size
        self.velocity = [0, 0]
        self.speed = [1, 1]
        self.grid_size = [1, 1]
        self.delta = [0, 0]
        self.direction = 1
        self.remain = 0
        self._animation = None

        self.rect = res[res_name][self.direction].get_rect()
        self.rect[:2] = coords

    def blit(self, res_file):
        image = self.res[self.res_file][self.direction]
        self.screen.blit(image, self.rect)

    # Movement
    def accelerate(self, x, y):
        self.velocity = add_lists(self.velocity, [x, y])

    def set_velocity(self, x, y):
        self.velocity = [x, y]

    def _apply_velocity(self):
        self.move(*self.velocity)

    def move(self, x, y):
        inp = mul_lists([x, y], self.speed)
        if self.grid():
            inp = mul_lists(inp, self.grid_size)

        self.delta = add_lists(
                self.delta,
                inp)

    def set_position(self, x, y):
        inp = [x, y]
        position = self.rect[:2]

        if self.grid():
            inp = mul_lists(inp, self.grid_size)
            position = mul_lists(position, self.grid_size)

        self.delta = sub_lists(inp, position)

    def _apply_position(self):
        self.rect[:2] = add_lists(self.rect[:2], self.delta)

        if self.delta[0] < 0:
            self.direction = 1 # left
        elif self.delta[0] > 0:
            self.direction = 3 # right

        self.delta = [0, 0]

    def grid(self):
        return self.grid_size != [1, 1]

    # Calculate final position
    def calculate(self):
        self._calculate()

    def _calculate(self):
        self._apply_velocity()
        self._apply_position()

    # Draw on screen
    def draw(self):
        raise NotImplementedError()

    def set_animation(self, animation):
        self._animation = animation

    def _draw_current(self):
        if self._animation:
            self.screen.blit(
                    self.res[self.res_name][self._animation.get_current()],
                    self.rect
                    )
        else:
            raise Exception('%s has no animation set' % self.__class__)

    def _draw_next(self):
        if self._animation:
            self.screen.blit(
                    self.res[self.res_name][self._animation.get_next()],
                    self.rect
                    )
        else:
            raise Exception('%s has no animation set' % self.__class__)
        return self._animation.beginning()

    def _draw_direction(self):
        self.screen.blit(self.res[self.res_name][self.direction], self.rect)

class DjinnGroup(pygame.sprite.Group):
    _named = {}

    def calculate(self):
        for sprite in self.sprites():
            sprite.calculate()

    def draw(self):
        to_flush = []
        for sprite in self.sprites():
            finished = sprite.draw()
            if finished:
                to_flush.append(sprite)
        return to_flush

    def collidepoint(self, x, y):
        results = []
        for sprite in self.sprites():
            if sprite.rect.collidepoint(x, y):
                results.append(sprite)
        return results

    def add_named(self, sprite, sprite_name):
        self._named[sprite_name] = sprite
        self.add(sprite)

    def get_named(self, sprite_name):
        if sprite_name in self._named:
            return self._named[sprite_name]

    def flush(self, to_flush):
        for sprite in to_flush:
            if self.has(sprite):
                self.remove(sprite)
