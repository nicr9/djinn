import pygame

class DjinnKeyboard(object):
    def process_keystroke(self):
        raise NotImplementedError

    def reset_keystroke(self):
        raise NotImplementedError

class SingleStepKeyboard(DjinnKeyboard):
    def process_keystroke(self, event):
        if self.debounce:
            if event.key == pygame.K_UP:
                self.player.move(0, -1)
            if event.key == pygame.K_DOWN:
                self.player.move(0, 1)
            if event.key == pygame.K_LEFT:
                self.player.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                self.player.move(1, 0)

    def reset_keystroke(self):
        pass

class KeepMovingKeyboard(DjinnKeyboard):
    moving = None

    def process_keystroke(self, event):
        if self.debounce:
            if event.key == pygame.K_UP:
                self.player.set_velocity(0, -1)
            if event.key == pygame.K_DOWN:
                self.player.set_velocity(0, 1)
            if event.key == pygame.K_LEFT:
                self.player.set_velocity(-1, 0)
            if event.key == pygame.K_RIGHT:
                self.player.set_velocity(1, 0)

            self.moving = event.key

    def reset_keystroke(self):
        if self.moving == pygame.K_UP:
            self.player.set_velocity(0, 1)
        if self.moving == pygame.K_DOWN:
            self.player.set_velocity(0, -1)
        if self.moving == pygame.K_LEFT:
            self.player.set_velocity(1, 0)
        if self.moving == pygame.K_RIGHT:
            self.player.set_velocity(-1, 0)

        self.moving = None
