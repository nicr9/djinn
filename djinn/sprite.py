from utils import mul_lists, add_lists, sub_lists
from djinn.utils import get_colour
import pygame

class DjinnSprite(pygame.sprite.Sprite):
    def __init__(self, res_store, res_name, coords):
        super(DjinnSprite, self).__init__()

        self.screen = res_store.screen
        self.res_store = res_store
        self.res_name = res_name

        self.config = res_store[res_name]

        self.remain = 0
        self.flush_time = None

        self.rect = coords + self.config.get_res(self.config.frame).size

    # Movement
    def accelerate(self, x, y):
        self.config.velocity = add_lists(self.config.velocity, [x, y])

    def set_velocity(self, x, y):
        self.config.velocity = [x, y]

    def _apply_velocity(self):
        self.move(*self.config.velocity)

    def move(self, x, y):
        inp = mul_lists([x, y], self.config.speed)
        if self.grid():
            inp = mul_lists(inp, self.config.grid)

        self.config.delta = add_lists(
                self.config.delta,
                inp)

    def set_position(self, x, y):
        inp = [x, y]
        position = self.rect[:2]

        if self.grid():
            inp = mul_lists(inp, self.config.grid)
            position = mul_lists(position, self.config.grid)

        self.config.delta = sub_lists(inp, position)

    def _apply_position(self):
        self.rect[:2] = add_lists(self.rect[:2], self.config.delta)

        if self.config.delta[0] < 0:
            self.config.direction = 1 # left
        elif self.config.delta[0] > 0:
            self.config.direction = 3 # right

        self.config.delta = [0, 0]

    def grid(self):
        return self.config.grid != [1, 1]

    # Calculate final position
    def calculate(self):
        self._calculate()

    def _calculate(self):
        self._apply_velocity()
        self._apply_position()

    def exited(self):
        x, y, w, h = self.rect
        sw, sh = self.screen.get_size()
        return (sw < x) or (x <= -w) or (sh < y) or (y <= -h)

    def at_bounds(self):
        x, y, w, h = self.rect
        sw, sh = self.screen.get_size()
        return ((sw - w) <= x) or (x <= 0) or ((sh - h) <= y) or (y <= 0)

    def for_flush(self):
        timed_out = False
        if not self.flush_time:
            return False
        if self.flush_time <= time.time():
            self.flush_time = None
            return self.exited or True

    # Draw on screen
    def draw(self):
        raise NotImplementedError()

    def set_animation(self, frame, start=0):
        self.config.frame = '%s.%d' % (frame, start)
        self.config.animated = True

    def set_frame(self, frame):
        self.config.frame = frame
        self.config.animated = False

    def next_frame(self):
        frame = self.config.frame
        if self.config.animated:
            new_frame = frame.split('.')
            new_frame[1] = int(new_frame[1]) + 1
            self.config.frame = '.'.join(new_frame)
        self.res_store[self.res_name][frame]

    def flush_in(self, secs):
        self.flush_time = time.time() + secs

class BitmapSprite(DjinnSprite):
    def _draw(self):
        image = self.next_frame()
        self.screen.blit(image, self.rect)

class DrawableSprite(DjinnSprite):

    def _draw(self):
        draw = self.next_frame()
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
                get_colour(colour),
                rect,
                border
                )

    def _draw_text(self, text, colour, coords):
        font = pygame.font.SysFont("monospace", 15)
        label = font.render(text, 1, get_colour(colour))
        self.screen.blit(label, coords)

class DjinnGroup(pygame.sprite.Group):
    _tagged = {}

    def __init__(self):
        super(DjinnGroup, self).__init__()

    def calculate(self):
        to_flush = []
        for sprite in self.sprites():
            sprite.calculate()
            if sprite.for_flush():
                to_flush.append(sprite)
        return to_flush

    def draw(self):
        for sprite in self.sprites():
            finished = sprite.draw()

    def collidepoint(self, x, y):
        results = []
        for sprite in self.sprites():
            if sprite.rect.collidepoint(x, y):
                results.append(sprite)
        return results

    def add_tagged(self, sprite, sprite_name):
        self._tagged[sprite_name] = sprite
        self.add(sprite)

    def get_tagged(self, sprite_name):
        if sprite_name in self._tagged:
            return self._tagged[sprite_name]

    def flush(self, to_flush):
        for sprite in to_flush:
            if self.has(sprite):
                self.remove(sprite)
