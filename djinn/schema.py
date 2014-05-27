from lament import *
from djinn.utils import add_lists

DEFAULT_SIZE = [32, 32]
DEFAULT_VELOCITY = [0, 0]
DEFAULT_SPEED = [1, 1]
DEFAULT_GRID = [1, 1]
DEFAULT_DELTA = [0, 0]
DEFAULT_FRAME = 'main'
DEFAULT_ANIMATED = False

def _bound(ins):
    if ins[0] == 'ellipse':
        return add_lists(ins[2][:2], ins[2][2:])
        # TODO: expand on this
    else:
        raise Exception("Unsupported draw tool: can't determine object size")

class BitmapRes(object):
    pass

class DrawableRes(object):
    def __init__(self, *args):
        self.instructions = args
        self.size = self._estimate_size()

    def _estimate_size(self):
        bounds = [_bound(ins) for ins in self.instructions]

        xs, ys = zip(*bounds)
        max_x = max(xs)
        max_y = max(ys)

        return [max_x, max_y]

    def __iter__(self):
        return self.instructions

class SpriteConf(LamentConfig):
    @regex_config('drawable', '.*', list)
    def drawable(self, old, new):
        return DrawableRes(*new)

    @regex_config('bitmap', '.*', list)
    def bitmap(self, old, new):
        return BitmapRes(*new)

    # Metadata
    @config('size', list)
    def size(self, old, new):
        return new

    @config('velocity', list)
    def velocity(self, old, new):
        return new

    @config('speed', list)
    def speed(self, old, new):
        return new

    @config('grid', list)
    def grid(self, old, new):
        return new

    @config('delta', list)
    def delta(self, old, new):
        return new

    @config('frame', str)
    def frame(self, old, new):
        return new

    @config('animated', bool)
    def animated(self, old, new):
        return new

    def get_res(self, res_name):
        if res_name in self.drawable:
            return self.drawable[res_name]
        elif res_name in self.bitmap:
            return self.bitmap[res_name]
        else:
            raise Exception("Resource not found")

