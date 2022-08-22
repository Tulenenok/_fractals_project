import random

class Tools:
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1
    SEPARATOR_COORDS = ' ; '
    SEPARATOR_POL = '---'
    INVALID_FILENAME = -1
    INVALID_LISTNAME = -2
    INVALID_HEAD = -3
    INVALID_DATA = -4
    INVALID_FORMAT_DATA = -5
    OBSCURE_ERROR = -6

    @staticmethod
    def isInt(x):
        try:
            x = int(x)
            return True
        except:
            return False

    @staticmethod
    def isFloat(x):
        try:
            x = float(x)
            return True
        except:
            return False

    @staticmethod
    def isRightFilename(filename):
        try:
            f = open(filename, 'r')
            f.close()
            return True
        except:
            return False

    @staticmethod
    def rgb_to_hex(r, g, b):
        rh = '0' + str(hex(int(r * 255))[2:].upper())
        gh = '0' + str(hex(int(g * 255))[2:].upper())
        bh = '0' + str(hex(int(b * 255))[2:].upper())
        return f'#{rh[-2:]}{gh[-2:]}{bh[-2:]}'

    @staticmethod
    def _from_rgb(rgb):
        return "#%02x%02x%02x" % rgb

    @staticmethod
    def _newColor(self):
        return self._from_rgb((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    @staticmethod
    def _newColor1(color):
        color = color[1:]
        rgb = list(int(color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = map(lambda x: x + (256 - x) // 4, rgb)
        return Tools.rgb_to_hex(r, g, b)