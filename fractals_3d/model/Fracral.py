import math, random

from controll.Tools import *
from model.Segment import *


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


class Fractal(BaseObj):
    def __init__(self, startX, startY, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, tag='fractal'):
        super().__init__()

        self.params = Params(startX, startY, startAlpha, delta, d, axiom, rules, n, color, width)
        self.segments = []
        self.updateShowFlag = False
        self.tag = tag

    def reShow(self, field, **p):
        if not self.segments:
            self.show(field)
        else:
            for seg in self.segments:
                seg.reShow(field)

    def show(self, field, needClean=True, showSteps=True):
        tmpParams = self.params.getCopy()
        stack = []
        for r in self.params.axiom:
            if r.isalpha():
                newX = tmpParams.x + tmpParams.step * math.cos(math.radians(tmpParams.alpha))
                newY = tmpParams.y + tmpParams.step * math.sin(math.radians(tmpParams.alpha))

                if r.isupper():
                    print('draw', tmpParams.x, tmpParams.y, newX, newY)
                    seg = Segment_2d(Point_2d(tmpParams.x, tmpParams.y), Point_2d(newX, newY),
                                     color=tmpParams.color,
                                     width=tmpParams.width, tag=self.tag)
                    seg.show(field)
                    self.segments.append(seg)

                    if showSteps:
                        field.update()

                tmpParams.x, tmpParams.y = newX, newY

            if r == '+':
                tmpParams.alpha += tmpParams.delta
            if r == '-':
                tmpParams.alpha -= tmpParams.delta
            if r == '[':
                stack.append(tmpParams.getCopy())
                print('push', tmpParams.x, tmpParams.y)
            if r == ']':
                tmpParams = stack.pop()
                print('pop', tmpParams.x, tmpParams.y)
            if r == '@':
                tmpParams.width = tmpParams.width * 0.8
                tmpParams.step = tmpParams.step * 0.8

        if not showSteps:
            field.update()

    def hide(self, field, **p):
        for seg in self.segments:
            seg.hide(field)
        self.segments.clear()


class FractalGenerate(BaseObj):
    def __init__(self, startX, startY, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, tag='fractal'):
        super(FractalGenerate, self).__init__()

        self.params = Params(startX, startY, startAlpha, delta, d, axiom, rules, n, color, width)
        self.n = self.params.n
        self.startAxiom = self.params.axiom

        self.updateShowFlag = False
        self.tag = tag

        self.lastFractal = None

    def show(self, field, needClear=True, showOnlyLast=False):
        try:
            field = field.canva
        except:
            pass

        for i in range(self.n):
            if self.lastFractal:
                self.lastFractal.hide(field)

            prm = self.params.getAll()

            if not showOnlyLast or i == self.n - 1:
                self.lastFractal = Fractal(*prm, self.tag, )
                self.lastFractal.show(field, needClear, showSteps=self.params.n <= 10)

            self.params.axiom = self._updateAxiom(self.params.axiom, self.params.rules)

    def hide(self, field, **param):
        try:
            field = field.canva
        except:
            pass
        finally:
            if self.lastFractal:
                self.lastFractal.hide(field)

    def reShow(self, field, **params):
        if self.lastFractal:
            self.lastFractal.reShow(field, **params)
        else:
            self.show(field, **params)


    def _updateAxiom(self, axiom, rules):
        newRule = []
        for r in axiom:
            if r in rules:
                newRule.append(rules[r])
            else:
                newRule.append(r)

        return ''.join(newRule)

