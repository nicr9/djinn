class DjinnConfine(object):
    def calculate(self, f):
        raise NotImplementedError

    def exited(self):
        for z in [X, Y]:
            if self.coords[z] > self.area[z]:
                return True
            if self.coords[z] < 0:
                return True
        return False

class BrickWallConfine(DjinnConfine):
    def calculate(self):
        last_coords = self.coords

        self._calculate()

        if self.exited():
            self.coords = last_coords

class BounceConfine(DjinnConfine):
    def calculate(self):
        self._calculate()
        for z in [X, Y]:
            if self.coords[z] > self.bounds[z]:
                self.coords[z] -= self.coords[z] - self.bounds[z]
                self.velocity[z] *= -1
            if self.coords[z] < 0:
                self.coords[z] *= -1
                self.velocity[z] *= -1

class AlertConfine(DjinnConfine):
    def calculate(self):
        self.calculate()
        return self.exited()
