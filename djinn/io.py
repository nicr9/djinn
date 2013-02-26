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
    def process_keystroke(self, event):
        if self.debounce:
            if event.key == pygame.K_UP:
                self.player.direction = [0, -1]
                self.player.set_velocity(0, -1)
            if event.key == pygame.K_DOWN:
                self.player.direction = [0, 1]
                self.player.set_velocity(0, 1)
            if event.key == pygame.K_LEFT:
                self.player.direction = [-1, 0]
                self.player.set_velocity(-1, 0)
            if event.key == pygame.K_RIGHT:
                self.player.direction = [1, 0]
                self.player.set_velocity(1, 0)

    def reset_keystroke(self):
        self.player.set_velocity(0, 0)

class DjinnMouse(object):
    def process_mouse(self, event):
        raise NotImplementedError

class JumpToMouse(DjinnMouse):
    def process_mouse(self, event):
        if self.m_debounce:
            self.player.set_position(*event.pos)
