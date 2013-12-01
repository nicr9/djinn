from os.path import isfile
from resource import Resources
from sprite import DjinnGroup
import pygame

class DjinnGame(object):
    player = None
    _groups = {}

    def __init__(self,
            window_size,
            window_caption,
            bg,
            refresh_rate,
            res):
        # Attributes
        self.window_size = window_size
        self.window_caption = window_caption
        self.bg = bg
        self.refresh_rate = refresh_rate
        self.counter = 0

        # Init
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()
        self.res = Resources(self.screen, res)
        self.register_group('_all_sprites', True)

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
        to_flush = self._groups['_all_sprites'].calculate()
        self.flush_sprites(to_flush)

    def draw_sprites(self):
        self._groups['_all_sprites'].draw()

    def register_group(self, group_name, flush=False):
        if group_name not in self._groups:
            self._groups[group_name] = DjinnGroup(flush)

    def flush_sprites(self, sprites):
        for group in self._groups.values():
            group.flush(sprites)

    def assign_sprite(self, sprite, group_name=None, sprite_name=None):
        if group_name is not None:
            groups = self._groups.setdefault(group_name, DjinnGroup())
            if sprite_name is None:
                groups.add(sprite)
            else:
                groups.add_named(sprite, sprite_name)

        if sprite not in self._groups['_all_sprites']:
            self._groups['_all_sprites'].add(sprite)

    def get_sprite(self, group_name, sprite_name):
        return self._groups[group_name].get_named(sprite_name)

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
