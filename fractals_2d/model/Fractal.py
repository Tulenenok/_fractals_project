import math, random

from model.Tools import *
from view.CanvasSegment import *

class Params:
    def __init__(self, startX, startY, startAlpha, delta, d, axiom, rules, n, color='blue', width=2):

        self.x, self.y, self.alpha = map(int, (startX, startY, startAlpha))
        self.step = float(d)
        self.delta = float(delta) if Tools.isFloat(delta) else eval(delta)
        self.axiom = axiom
        self.rules = rules if type(rules) == dict else eval('{' + str(rules) + '}')
        self.n = int(n)
        self.color, self.width = color, int(width)

    def getAll(self):
        return self.x, self.y, self.alpha, self.delta, self.step, self.axiom, self.rules, self.n, self.color, self.width

    def getCopy(self):
        return Params(*self.getAll())


class Fractal:
    def __init__(self, startX, startY, startAlpha, delta, d, axiom, rules, n, color='blue', width=2):
        self.params = Params(startX, startY, startAlpha, delta, d, axiom, rules, n, color, width)
        self.segments = []
        self.updateShowFlag = False

    def reShow(self, field):
        if not self.segments:
            self.show(field)
        else:
            for seg in self.segments:
                seg.reShow(field)

    def show(self, field, needClean=False):
        rule = self.params.axiom
        stack = []

        tmpParams = self.params.getCopy()

        self.segments.clear()
        for i in range(self.params.n):
            if needClean:
                field.canva.clear()
                tmpParams = self.params.getCopy()
            for r in rule:
                if r.isalpha():
                    newX = tmpParams.x + tmpParams.step * math.cos(math.radians(tmpParams.alpha))
                    newY = tmpParams.y + tmpParams.step * math.sin(math.radians(tmpParams.alpha))
                    if r.isupper():
                        seg = CanvasSegment(Point_2d(tmpParams.x, tmpParams.y), Point_2d(newX, newY), color=tmpParams.color, width=tmpParams.width)
                        seg.show(field.canva)
                        if self.params.n < 10:
                            field.canva.update()
                        if i == self.params.n - 1:
                            self.segments.append(seg)
                    tmpParams.x, tmpParams.y = newX, newY
                if r == '+':
                    tmpParams.alpha += tmpParams.delta
                if r == '-':
                    tmpParams.alpha -= tmpParams.delta
                if r == '[':
                    stack.append(tmpParams.getCopy())
                if r == ']':
                    tmpParams = stack.pop()
                if r == '@':
                    tmpParams.width = tmpParams.width * 0.8
                    tmpParams.step = tmpParams.step * 0.8

            if self.params.n >= 10:
                field.canva.update()

            rule = self._changeRule(rule, tmpParams.rules)

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb

    def _newColor(self):
        return self._from_rgb((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def _newColor1(self, color):
        color = color[1:]
        rgb = list(int(color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = map(lambda x: x + (256 - x) // 4, rgb)
        return Tools.rgb_to_hex(r, g, b)

    def _changeRule(self, rule, aksiom):
        newRule = []
        for r in rule:
            if r in aksiom:
                newRule.append(aksiom[r])
            else:
                newRule.append(r)

        return ''.join(newRule)
