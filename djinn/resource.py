import os, re, json, pygame
from utils import Colours

class Resources(object):
    # Regexs
    res_re = re.compile('(.*)\.dj$')
    face_re = "%s_(.*).bmp"

    # _res[resource_name][face_number] -> pygame.Surface
    _res = {}

    def __init__(self, screen, res_path):
        # Stash the screen surface
        self.screen = screen

        # Walk the provided path looking for .dj files
        for root, dirs, files in os.walk(res_path):
            match = re.search(self.res_re, root)
            if match:
                # Add .dj file to _res
                res_name = os.path.basename(match.group(1))
                self._res[res_name] = {}

                # Each .bmp in the .dj represents a different 'face'
                for f in files:
                    bmp_ex = self.face_re % res_name
                    face_file = re.match(bmp_ex, f)
                    if face_file:
                        face_varient = face_file.group(1)
                        full_path = os.path.join(root, f)
                        temp = pygame.image.load(full_path).convert()
                        temp.set_colorkey(Colours.black)
                        self._res[res_name][int(face_varient)] = temp
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
