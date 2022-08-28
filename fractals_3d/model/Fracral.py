import math, random, copy

from model.Figure import *
from model.Params import *


class Fractal(Figure):
    def __init__(self, startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, constants=[], tag='fractal'):
        super().__init__()

        self.params = Params(startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color, width, constants=constants)
        self.segments = []
        self.updateShowFlag = False
        self.paramsSegments = dict()
        self.needCalc = True
        self.tag = tag

    def reShow(self, field, **p):
        super(Fractal, self).reShow(field)

    def calculate(self, showInRealTime=False, showSteps=True, field=None):
        tmp = copy.deepcopy(self.params)

        stack = []
        vertex, links = [(tmp.x, tmp.y, tmp.z)], []

        i, j = 1, 2

        findOpen = False
        for r in self.params.axiom:
            if findOpen or r == '(' or r == '(':
                findOpen = r != ')'
                continue

            if r.isalpha() and r not in tmp.constants:
                newX = tmp.x + tmp.step * tmp.HLU[0, 0]
                newY = tmp.y + tmp.step * tmp.HLU[0, 1]
                newZ = tmp.z + tmp.step * tmp.HLU[0, 2]

                if r.isupper():
                    if showInRealTime:
                        seg = Segment_2d(Vector_3d(tmp.x, tmp.y, tmp.z), Vector_3d(newX, newY, newZ),
                                         color=tmp.color,
                                         width=tmp.width, tag=self.tag)
                        seg.show(field)
                        self.segments.append(seg)

                        if showSteps:
                            field.update()

                    vertex.append((newX, newY, newZ))
                    links += [i, j]
                    self.paramsSegments[f'{i}, {j}'] = (tmp.color, tmp.width)
                    i = j
                    j += 1

                tmp.x, tmp.y, tmp.z = newX, newY, newZ

            elif r == '+':
                tmp.rotate(math.radians(tmp.delta), 'U')
            elif r == '-':
                tmp.rotate(math.radians(-tmp.delta), 'U')
            elif r == '&' or r == '_':
                tmp.rotate(math.radians(tmp.delta), 'L')
            elif r == '^':
                tmp.rotate(math.radians(-tmp.delta), 'L')
            elif r == '|':
                tmp.rotate(math.radians(tmp.delta), 'H')
            elif r == '/':
                tmp.rotate(math.radians(-tmp.delta), 'H')
            elif r == '\\':
                tmp.rotate(math.radians(180), 'U')

            elif r == '[':
                stack.append((i, copy.deepcopy(tmp)))
            elif r == ']':
                i, tmp = stack.pop()

            elif r == '@':
                tmp.width = tmp.width * 0.8
                tmp.step = tmp.step * 0.8

        if not showSteps and showInRealTime:
            field.update()

        self.fillVert(vertex)
        self.fillPol(links)

    def show(self, field, needClean=True, showSteps=True):
        if self.needCalc:
            self.calculate(False, showSteps, field)
            self.needCalc = False
        super(Fractal, self).show(field)

    def hide(self, field, **p):
        for seg in self.segments:
            seg.hide(field)
        self.segments.clear()



class FractalGenerate(BaseObj):
    def __init__(self, startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, constants=[], tag='fractal'):
        super(FractalGenerate, self).__init__()

        self.params = Params(startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color, width, constants)
        self.n = self.params.n
        self.startAxiom = self.params.axiom

        self.updateShowFlag = False
        self.tag = tag

        self.lastFractal = None

    def show(self, field, needClear=True, showOnlyLast=True):
        try:
            field = field.canva
        except:
            pass

        for i in range(self.n):
            if self.lastFractal:
                self.lastFractal.hide(field)

            prm = self.params.getAll()

            if not showOnlyLast or i == self.n - 1:
                self.lastFractal = Fractal(*prm, self.tag )
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
        def countParams(i, axiom):
            if i == len(axiom) - 1 or axiom[i + 1] != '(':
                return i, 0, []

            startInd, endInd = i + 2, i + 2
            while axiom[endInd] != ')':
                endInd += 1

            params = axiom[startInd: endInd].split(',')
            for j, p in enumerate(params):
                params[j] = eval(str(p))

            return endInd, len(params), params

        newRule = []
        i = 0
        while i < len(axiom):
            r = axiom[i]
            f = True
            if r in rules:
                i, count, params = countParams(i, axiom)
                if count in rules[r]:
                    prm, cond, child = rules[r][count]
                    dct = dict()
                    for j, key in enumerate(prm):
                        dct[key] = params[j]
                        child = child.replace(key, str(params[j]))

                    if eval(cond, dct):
                        newRule.append(child)
                        f = False
            if f:
                newRule.append(r)
            i += 1

        return ''.join(newRule)