import math, random
from view.CanvasSegment import *


class Fractal:
    def __init__(self, startX=0, startY=0, startAlpha=90, delta=22.5, d=2, axiom='F',
                       rules={}, n=5, color='blue', width=2):

        self.x, self.y, self.alpha = startX, startY, startAlpha
        self.delta, self.step = delta, d
        self.axiom, self.rules = axiom, rules
        self.n = n
        self.color, self.width = color, width

        self.segments = []
        self.updateShowFlag = False

    def reShow(self, field):
        if not self.segments:
            self.show(field)
        else:
            for seg in self.segments:
                seg.reShow(field)

    def show(self, field, needClean=True):
        rule = self.axiom
        stack = []

        x, y, alpha, d, delta = self.x, self.y, self.alpha, self.step, self.delta
        for i in range(self.n):
            if needClean:
                field.canva.clear()
                x, y, alpha = self.x, self.y, self.alpha
                self.segments.clear()
            for r in rule:
                if r in 'FfLlRrXx':
                    newX = x + d * math.cos(math.radians(alpha))
                    newY = y + d * math.sin(math.radians(alpha))
                    if r in 'FLRX':
                        seg = CanvasSegment(CanvasPoint(x, y), CanvasPoint(newX, newY), color=self.color, width=self.width)
                        seg.show(field.canva)
                        field.canva.update()
                        self.segments.append(seg)
                    x, y = newX, newY
                if r == '+':
                    alpha += delta
                if r == '-':
                    alpha -= delta
                if r == '[':
                    stack.append((x, y, alpha))
                if r == ']':
                    x, y, alpha = stack.pop()

            rule = self._changeRule(rule, self.rules)

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb

    def _newColor(self):
        return self._from_rgb((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def _changeRule(self, rule, aksiom):
        newRule = []
        for r in rule:
            if r in aksiom:
                newRule.append(aksiom[r])
            else:
                newRule.append(r)

        return ''.join(newRule)
