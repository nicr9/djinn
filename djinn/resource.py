import os, re, json, pygame
from utils import Colours

class Resources(object):
    res_re = re.compile('(.*)\.dj$')
    wnes = ['west', 'north', 'east', 'south']
    _res = {}

    def __init__(self, screen, res_path):
        self.screen = screen
        for root, dirs, files in os.walk(res_path):
            match = re.search(self.res_re, root)
            if match:
                # Add .dj file to _res
                res_name = os.path.basename(match.group(1))
                self._res[res_name] = {}

                # Open each .bmp in .dj
                wnes_re = "%s_([1-4]).bmp"
                for f in files:
                    bmp_ex = wnes_re % res_name
                    direction_file = re.match(bmp_ex, f)
                    if direction_file:
                        facing = direction_file.group(1)
                        full_path = os.path.join(root, f)
                        temp = pygame.image.load(full_path).convert()
                        temp.set_colorkey(Colours.black)
                        self._res[res_name][int(facing)] = temp
            else:
                continue

            for key, val in self._res.iteritems():
                print "%s: %s" % (key, val)

    def __getitem__(self, key):
        try:
            return self._res[key]
        except KeyError, e:
            raise Exception('Resource missing: %s' % key)

if __name__ == "__main__":
    screen = pygame.display.set_mode([50, 50])
    pygame.display.set_caption("Resources Test...")
    Resources(screen, 'res/mario.dj')
