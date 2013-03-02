import pygame
from inspect import isfunction

class DjinnKeyboard(object):
    _key_handlers = {}
    _active_keys = []

    def register_keys(self):
        raise NotImplementedError()

    def _register(self, key, f):
        if isinstance(f, tuple) and len(f) == 2:
            self._key_handlers[key] = f
        elif isfunction(f):
            self._key_handlers[key] = f
        else:
            raise AttributeError()

    def _update_keys(self):
        keys = pygame.key.get_pressed()

        for key, state in enumerate(keys):
            if state and key not in self._active_keys:
                # Handle key
                self._active_keys.append(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]
                    if isinstance(handle, tuple) and len(handle) == 2:
                        self.player.accelerate(*handle)
            elif not state and key in self._active_keys:
                # Undo key
                self._active_keys.remove(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]
                    if isinstance(handle, tuple) and len(handle) == 2:
                        counter = [-1 * z for z in handle]
                        self.player.accelerate(*counter)

class BasicKeyboard(DjinnKeyboard):
    def register_keys(self):
        self._register(pygame.K_UP, (0, -1))
        self._register(pygame.K_DOWN, (0, 1))
        self._register(pygame.K_LEFT, (-1, 0))
        self._register(pygame.K_RIGHT, (1, 0))

class DjinnMouse(object):
    def process_mouse(self, event):
        raise NotImplementedError

class JumpToMouse(DjinnMouse):
    def process_mouse(self, event):
        if self.m_debounce:
            self.player.set_position(*event.pos)
