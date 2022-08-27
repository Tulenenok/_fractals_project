from controll.Tools import *


class Params:
    def __init__(self, startX, startY, startZ,
                 startAlpha,
                 delta, d,
                 axiom, rules,
                 n, color='blue', width=2):

        self.x, self.y = startX, startY
        self.z = startZ
        self.alpha = startAlpha
        self.step = float(d)
        self.delta = float(delta) if Tools.isFloat(delta) else eval(delta)
        self.axiom = axiom
        self.rules = rules if type(rules) == dict else eval('{' + str(rules) + '}')
        self.n = int(n)
        self.color, self.width = color, int(width)

    def __getattribute__(self, item):
        if item == 'x' or item == 'y' or item == 'z' or item == 'alpha':
            tmp = object.__getattribute__(self, item)
            return int(tmp) if Tools.isFloat(tmp) else eval(tmp)
        else:
            return object.__getattribute__(self, item)

    def getAll(self):
        return self.x, self.y, self.z, self.alpha, self.delta, self.step, self.axiom, self.rules, self.n, self.color, self.width

    def getCopy(self):
        return Params(*self.getAll())
