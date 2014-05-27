import os, re, json, pygame, sys
from os.path import isdir
from djinn.schema import SpriteConf
from djinn.utils import get_colour

class Resources(object):
    # Regexs
    res_re = re.compile('^(.*)\.dj$')

    # _res[resource_name][face_number] -> pygame.Surface
    _res = {}

    def __init__(self, screen, res_dir):
        # Stash the screen surface
        self.screen = screen

        # Ensure res path exists
        if not isdir(res_dir):
            print "Whoops, can't find game resources!"
            sys.exit()

        # Walk the provided path looking for .dj files
        for root, dirs, files in os.walk(res_dir):
            for res in files:
                match = re.match(self.res_re, res)
                if match:
                    # Add .dj file to _res
                    res_name = os.path.basename(match.group(1))
                    res_path = os.path.join(root, res)
                    self._res[res_name] = SpriteConf.from_file(res_path)

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
    Resources(screen, 'res/')
