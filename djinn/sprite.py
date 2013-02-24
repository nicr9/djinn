from utils import mul_lists, add_lists, sub_lists
# Base classes
class DjinnSprite(object):
    grid_size = [1, 1]
    speed = [1, 1]
    delta = [0, 0]

    def __init__(self, screen, colour, coords, size, velocity):
        self.screen = screen
        self.colour = colour
        self.coords = mul_lists(
                coords,
                self.grid_size)
        self.size = size
        self.velocity = velocity

        self.area = self.screen.get_size()
        self.bounds = sub_lists(self.area, self.size)

    # Movement
    def accelerate(self, x, y):
        self.velocity = add_lists(self.velocity, [x, y])

    def set_velocity(self, x, y):
        self.velocity = [x, y]

    def _apply_velocity(self):
        self.move(*self.velocity)

    def move(self, x, y):
        inp = mul_lists([x, y], self.speed)
        if self.grid():
            inp = mul_lists(inp, self.grid_size)

        self.delta = add_lists(
                self.delta,
                inp)

    def set_position(self, x, y):
        inp = [x, y]
        position = self.coords

        if self.grid():
            inp = mul_lists(inp, self.grid_size)
            position = mul_lists(position, self.grid_size)

        self.delta = sub_lists(inp, position)

    def _apply_position(self):
        self.coords = add_lists(self.coords, self.delta)
        self.delta = [0, 0]

    def grid(self):
        return self.grid_size != [1, 1]

    # Calculate final position
    def calculate(self):
        self._calculate()

    def _calculate(self):
        self._apply_velocity()
        self._apply_position()

    # Draw on screen
    def draw(self):
        raise NotImplementedError()