# Utility functions
def sub_lists(a, b):
    assert len(a) == len(b)
    return [(x - y) for x, y in zip(a, b)]

def add_lists(a, b):
    assert len(a) == len(b)
    return [(x + y) for x, y in zip(a, b)]

def mul_lists(a, b):
    assert len(a) == len(b)
    return [(x * y) for x, y in zip(a, b)]

def div_lists(a, b):
    assert len(a) == len(b)
    return [(x / y) for x, y in zip(a, b)]

# Utility classes
class Colours(object):
    white = [255, 255, 255]
    black = [0, 0, 0]
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]

pi = 3.14159
X, Y = 0, 1
