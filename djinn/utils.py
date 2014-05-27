from random import randrange

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

COLOURS = {
        'red': [255, 0, 0],
        'green': [0, 255, 0],
        'blue': [0, 0, 255],
        'black': [0, 0, 0],
        'white': [255, 255, 255],
        'random': [randrange(255), randrange(255), randrange(255)],
        'randomgrey': [randrange(255)] * 3,
        }

def get_colour(name):
    return COLOURS[name]

pi = 3.14159
X, Y = 0, 1
