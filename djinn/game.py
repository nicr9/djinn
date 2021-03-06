from os.path import isfile
from djinn.resource import Resources
from djinn.sprite import DjinnGroup
from djinn.utils import get_colour
from collections import defaultdict
import pygame

class DjinnGame(object):

    def __init__(self,
            window_size,
            window_caption,
            bg,
            refresh_rate,
            res_path):
        # Attributes
        self.window_size = window_size
        self.window_caption = window_caption
        self.bg = get_colour(bg)
        self.refresh_rate = refresh_rate
        self.counter = 0

        # Setup sprite stuff
        self.player = None
        self._groups = defaultdict(DjinnGroup)

        # Init
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()
        self.res_store = Resources(self.screen, res_path)

    # Background handling
    def draw_bg(self):
        if isinstance(self.bg, list):
            self.screen.fill(self.bg)
        elif isinstance(self.bg, pygame.Surface):
            self.screen.blit(self.bg, [0, 0])
        elif isinstance(self.bg, str):
            if isfile(self.bg):
                self.bg = pygame.image.load(self.bg).convert()
                self.draw_bg()
            else:
                raise Exception("What's this? : %s" % self.bg)
        else:
            raise Exception("What's this? : %s" % self.bg)

    # Sprite handling
    def load_sprites(self):
        raise NotImplementedError()

    def move_sprites(self):
        to_flush = self._groups['_active'].calculate()
        self.flush_sprites(to_flush)

    def draw_sprites(self):
        self._groups['_active'].draw()

    def flush_sprites(self, sprites, group_name='_active'):
        self._groups[group_name].flush(sprites)

    def show_sprite(self, sprite):
        if sprite not in self._groups['_active']:
            self._groups['_active'].add(sprite)

    def assign_sprite(self, sprite, group_name, tag=''):
        if tag:
            self._groups[group_name].add_tagged(sprite, tag)
        else:
            self._groups[group_name].add(sprite)

    def get_sprite(self, group_name, tag):
        return self._groups[group_name].get_tagged(tag)

    # IO
    def register_keys(self):
        pass

    def _update_keys(self):
        pass

    def process_mouse(self, event):
        pass

    # Hooks
    def pre_draw(self):
        pass

    # Mainloop
    def go(self):
        self.load_sprites()

        self.register_keys()

        self.debounce = True
        self.m_debounce = True
        done = False
        while not done:
            # User input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
                    self._update_keys()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.process_mouse(event)
                    self.m_debounce = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.m_debounce = True

            # Calculate positions
            self.move_sprites()

            # pre_draw events
            self.pre_draw()

            # Draw results
            self.draw_bg()
            self.draw_sprites()
            pygame.display.flip()

            self.clock.tick(self.refresh_rate)
            self.counter += 1

        pygame.quit()
