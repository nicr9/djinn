class DjinnConfine(object):
    def confine(self, f):
        raise NotImplementedError

class BrickWallConfine(DjinnConfine):
    def confine(self, f):
        last_coords = self.coords

        f()

        if self.exited():
            self.coords = last_coords
