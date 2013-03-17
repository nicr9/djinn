class DjinnAnimation(object):
    def __init__(self, action=None, frames=None):
        self._actions = {}
        self._current_action = None
        pointer = 0

        if action is not None and frames is not None:
            self.add_action(action, frames)

    def add_action(self, action, frames):
        self._actions[action] = frames

        if self._current_action is None:
            self.set_action(action)

    def set_action(self, action):
        self._current_action = action
        self.pointer = 0
        self._action_len = len(self._actions[action])

    def next(self):
        self.pointer = (self.pointer + 1) % self._action_len

    def get_current(self):
        return self._actions[self._current_action][self.pointer]

    def get_next(self):
        temp = self._actions[self._current_action][self.pointer]
        self.next()
        return temp
