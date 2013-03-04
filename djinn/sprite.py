from utils import mul_lists, add_lists, sub_lists
import pygame
from os.path import isfile

class DjinnSprite(pygame.sprite.Sprite):
    def __init__(self, screen, res, coords, size=[16, 16]):
        super(DjinnSprite, self).__init__()
        self.screen = screen
        self.size = size
        self.velocity = [0, 0]
        self.speed = [1, 1]
        self.grid_size = [1, 1]
        self.delta = [0, 0]
        self.direction = [0, 1]

        if isinstance(res, str) and isfile(res):
            self.image = pygame.image.load(res).convert()
        elif isinstance(res, list):
            self.image = pygame.Surface(tuple(size))
            self.image.fill(res)
        elif isinstance(res, pygame.Surface):
            self.image = res
        else:
            raise Exception('Faulty res')

        self.rect = self.image.get_rect()
        self.rect[:2] = coords

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

class DjinnGroup(pygame.sprite.Group):
    pass
