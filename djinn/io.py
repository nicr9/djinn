import pygame

class DjinnKeyboard(object):
    _key_handlers = {}
    _key_states = [] # TODO: refactor: _active_keys

    def register_keys(self):
        raise NotImplementedError()

    # TODO: add a register method

    def _update_keys(self):
        keys = pygame.key.get_pressed()

        for key, state in enumerate(keys):
            if state and key not in self._key_states:
                # Handle key
                self._key_states.append(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]
                    if isinstance(handle, tuple) and len(handle) == 2:
                        self.player.accelerate(*handle)
            elif not state and key in self._key_states:
                # Undo key
                self._key_states.remove(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]
                    if isinstance(handle, tuple) and len(handle) == 2:
                        counter = [-1 * z for z in handle]
                        self.player.accelerate(*counter)

class BasicKeyboard(DjinnKeyboard):
    def register_keys(self):
        self._key_handlers = {pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)}

class DjinnMouse(object):
    def process_mouse(self, event):
        raise NotImplementedError

class JumpToMouse(DjinnMouse):
    def process_mouse(self, event):
        if self.m_debounce:
            self.player.set_position(*event.pos)
