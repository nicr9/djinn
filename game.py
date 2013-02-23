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

        # Variables
        self.player_x = 0
        self.player_y = 0

        # Init
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()

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

    def load_sprites(self):
        raise NotImplementedError()
        self.b = Box(self.screen, Colours.white)

    def move_sprites(self):
        raise NotImplementedError()

    def move_player(self):
        if self.player:
           self.player.drift()

    def draw_sprites(self):
        raise NotImplementedError()

    def draw_player(self):
        if self.player:
            self.player.draw()

    def process_mouse(self, event):
        if self.m_debounce:
            self.player.move_raw(*event.pos)

    def go(self):
        self.load_sprites()

        self.debounce = True
        self.m_debounce = True
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                if event.type == pygame.KEYDOWN:
                    self.process_keystroke(event)
                    self.debounce = False
                if event.type == pygame.KEYUP:
                    self.reset_keystroke()
                    self.debounce = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.process_mouse(event)
                    self.m_debounce = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.m_debounce = True

            self.move_sprites()
            self.move_player()

            self.draw_bg()
            self.draw_sprites()
            self.draw_player()
            pygame.display.flip()

            self.clock.tick(self.refresh_rate)

        pygame.quit()