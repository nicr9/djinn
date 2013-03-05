from utils import X, Y

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

    def exited_via(self):
        area = self.screen.get_size()

        # w = 1, n = 2, e = 3, s = 4
        for z in [X, Y]:
            if self.rect[z] > area[z]:
                return z + 3
            if self.rect[z] < 0:
                return z + 1

        # hasn't left the screen
        return 0

class DonutConfine(DjinnConfine):
    def calculate(self):
        last_coords = self.rect[:2]

        self._calculate()

        exit = self.exited_via()
        area = self.screen.get_size()

        if exit == 1:
            self.rect[0] = area[0]
        elif exit == 2:
            self.rect[1] = area[1]
        elif exit == 3:
            self.rect[0] = 0
        elif exit == 4:
            self.rect[1] = 0

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

        bounds = sub_lists(self.screen.get_size(), self.rect[2:])

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
