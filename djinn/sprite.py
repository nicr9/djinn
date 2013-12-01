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
        self.animation = None

        self.rect = res[res_name][self.direction].get_rect()
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

    def exited(self):
        x, y, w, h = self.rect
        sw, sh = self.screen.get_size()

        return (w < x < -w) or (h < y < -h)

    # Draw on screen
    def draw(self):
        raise NotImplementedError()

    def set_animation(self, animation_name, state=None):
        self.animation = animation_name

        if state is not None:
            self.animation.set_active(state)

class BitmapSprite(DjinnSprite):
    def _blit(self, res_indx):
        image = self.res[self.res_name][res_indx]
        self.screen.blit(image, self.rect)

    def _draw_w_animate(self):
        if self.animation:
            if self.animation.is_active():
                self._blit(self.animation.get_next())
            else:
                self._blit(self.animation.get_current())
        else:
            self._blit(0)
        return self.animation.beginning()

    def _draw_direction(self):
        self._blit(self.direction)

class DrawableSprite(DjinnSprite):
    def _draw_instruction(self, instruction):
        tool = instruction[0]
        args = instruction[1:]

        if tool == 'ellipse':
            self._draw_ellipse(*args)
        elif tool == 'text':
            self._draw_text(*args)
        #if tool == 'rect':
        #    self._draw_rect(*args)
        #if tool == 'line':
        #    self._draw_line(*args)
        else:
            raise Exception('Bad instruction: %s' (instruction, ))

    def _draw_ellipse(self, colour, rect_offset, border):
        rect = add_lists(self.rect[:2], rect_offset[:2]) + rect_offset[2:]

        pygame.draw.ellipse(
                self.screen,
                colour,
                rect,
                border
                )

    def _draw_text(self, text, colour, coords):
        label = pygame.font.SysFont("monospace", 15).render(text, 1, colour)
        self.screen.blit(label, coords)

class DjinnGroup(pygame.sprite.Group):
    _named = {}

    def __init__(self, flush=False):
        super(DjinnGroup, self).__init__()
        self._flush = flush

    def calculate(self):
        left_screen = []
        for sprite in self.sprites():
            sprite.calculate()
            if sprite.exited():
                left_screen.append(sprite)
        return left_screen

    def draw(self):
        for sprite in self.sprites():
            finished = sprite.draw()

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
        if self._flush:
            for sprite in to_flush:
                if self.has(sprite):
                    self.remove(sprite)
