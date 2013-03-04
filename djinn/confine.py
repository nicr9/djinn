class DjinnConfine(object):
    def calculate(self, f):
        raise NotImplementedError

    def exited(self):
        area = self.screen.get_size()

        for z in [X, Y]:
            if self.rect[z] > area[z]:
                return True
            if self.rect[z] < 0:
                return True
        return False

class BrickWallConfine(DjinnConfine):
    def calculate(self):
        last_coords = self.rect[:2]

        self._calculate()

        if self.exited():
            # Block from exiting by keeping coords the same
            self.rect[:2] = last_coords

class BounceConfine(DjinnConfine):
    def calculate(self):
        self._calculate()

        bounds = sub_lists(self.screen.get_size(), self.rect[2:]

        for z in [X, Y]:
            if self.rect[z] > bounds[z]:
                self.rect[z] -= self.rect[z] - bounds[z]
                self.velocity[z] *= -1
            if self.rect[z] < 0:
                self.rect[z] *= -1
                self.velocity[z] *= -1

class AlertConfine(DjinnConfine):
    def calculate(self):
        self.calculate()
        return self.exited()
