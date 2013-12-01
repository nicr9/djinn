import pygame
from inspect import isfunction

class DjinnKeyboard(object):
    _key_handlers = {}
    _key_sprite_map = {}
    _active_keys = []

    def register_keys(self):
        raise NotImplementedError()

    def _register(self, key, f, sprite=None):
        if isinstance(f, tuple) and len(f) == 2:
            self._key_handlers[key] = f
        elif hasattr(f, '__call__'):
            self._key_handlers[key] = f
        else:
            raise AttributeError()

        if sprite is not None:
            self._key_sprite_map[key] = sprite

    def _update_keys(self):
        keys = pygame.key.get_pressed()

        for key, state in enumerate(keys):
            if state and key not in self._active_keys:

                # Handle key
                self._active_keys.append(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]

                    sprite = None
                    if key in self._key_sprite_map:
                        sprite = self._key_sprite_map[key]

                    # Move sprite
                    if isinstance(handle, tuple) and len(handle) == 2:
                        if sprite:
                            sprite.accelerate(*handle)
                        else:
                            raise Exception(
                                    'Moving the bg is not currently supported'
                                    )

                    # Call handler
                    elif hasattr(handle, '__call__'):
                        handle(True, sprite)
                    else:
                        raise Exception()

            elif not state and key in self._active_keys:

                # Undo key
                self._active_keys.remove(key)
                if key in self._key_handlers:
                    handle = self._key_handlers[key]

                    sprite = None
                    if key in self._key_sprite_map:
                        sprite = self._key_sprite_map[key]

                    # Stop player
                    if isinstance(handle, tuple) and len(handle) == 2:
                        if sprite:
                            counter = [-1 * z for z in handle]
                            sprite.accelerate(*counter)
                        else:
                            pass

                    # Call handler
                    elif isfunction(handle):
                        handle(False, sprite)
                    else:
                        raise Exception()

class BasicKeyboard(DjinnKeyboard):
    def register_keys(self, sprite=None):
        self._register(pygame.K_UP, (0, -1), sprite)
        self._register(pygame.K_DOWN, (0, 1), sprite)
        self._register(pygame.K_LEFT, (-1, 0), sprite)
        self._register(pygame.K_RIGHT, (1, 0), sprite)

class DjinnMouse(object):
    def process_mouse(self, event):
        raise NotImplementedError

class JumpToMouse(DjinnMouse):
    def process_mouse(self, event):
        if self.m_debounce:
            self.player.set_position(*event.pos)
