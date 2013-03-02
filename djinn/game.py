from os.path import isfile
import pygame

class DjinnGame(object):
    player = None

    def __init__(self,
            window_size,
            window_caption,
            bg,
            refresh_rate):
        # Attributes
        self.window_size = window_size
        self.window_caption = window_caption
        self.bg = bg
        self.refresh_rate = refresh_rate

        # Init
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()
        self.counter = 0

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
        raise NotImplementedError()

    def draw_sprites(self):
        raise NotImplementedError()

    # Player sprite handling
    def load_player(self):
        raise NotImplementedError()

    def move_player(self):
        if self.player:
            self.player.calculate()

    def draw_player(self):
        if self.player:
            self.player.draw()

    # IO
    def register_keys(self):
        pass

    def _update_keys(self):
        pass

    def process_mouse(self, event):
        pass

    # Mainloop
    def go(self):
        self.load_sprites()
        self.load_player()

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
            self.move_player()

            # Draw results
            self.draw_bg()
            self.draw_sprites()
            self.draw_player()
            pygame.display.flip()

            self.clock.tick(self.refresh_rate)
            self.counter += 1

        pygame.quit()
