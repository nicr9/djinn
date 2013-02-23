# Base classes
class DjinnSprite(object):
    GRID = 1
    DEBOUNCE = False
    
    def __init__(self, screen, colour, coords, size, velocity):
        self.screen = screen
        self.colour = colour
        self.coords = mul_lists(
                coords,
                [self.GRID, self.GRID])
        self.size = size
        self.velocity = velocity

        self.area = self.screen.get_size()
        self.bounds = sub_lists(self.area, self.size)

    def drift(self):
        if self.GRID != 1:
            print "Sprites can't drift if on a grid" # FIXME:
        self.coords = add_lists(self.coords, self.velocity)
        if self.CONFINED:
            self.bounce()
        else:
            return self.exited()

    def move_raw(self, x, y):
        last_coords = self.coords

        self.coords = sub_lists([x, y], [x%self.GRID, y%self.GRID])
        if self.exited():
            self.coords = last_coords

    def move(self, x, y):
        last_coords = self.coords

        self.coords = add_lists(
                self.coords,
                (x, y))
        if self.exited():
            self.coords = last_coords

    def impulse(self, x, y):
        self.velocity = add_lists(self.velocity, [x, y])

    def exited(self):
        for z in [X, Y]:
            if self.coords[z] > self.area[z]:
                return True
            if self.coords[z] < 0:
                return True
        return False

    def bounce(self):
        for z in [X, Y]:
            if self.coords[z] > self.bounds[z]:
                self.coords[z] -= self.coords[z] - self.bounds[z]
                self.velocity[z] *= -1
            if self.coords[z] < 0:
                self.coords[z] *= -1
                self.velocity[z] *= -1

    def draw(self):
        raise NotImplementedError()

    @MixinWarn('DjinnConfine')
    def confine(self, f):
        f()

class DjinnGridSprite(DjinnSprite):
    def __init__(self, screen, bg, coords, grid_size, velocity):
        self.GRID = grid_size
        super(DjinnGridSprite, self).__init__(
                screen,
                bg,
                coords,
                [grid_size, grid_size],
                velocity)

    def move(self, x, y):
        super(DjinnGridSprite, self).move(x*self.GRID, y*self.GRID)
