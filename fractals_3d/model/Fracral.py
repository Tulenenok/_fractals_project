import math, random, copy

from model.Figure import *
from model.Params import *


class Fractal(Figure):
    def __init__(self, startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, tag='fractal'):
        super().__init__()

        self.params = Params(startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color, width)
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

        for r in self.params.axiom:
            print(r)
            print(np.matrix(tmp.HLU, dtype='int32'))
            if r.isalpha():
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

            if r == '+':
                tmp.rotate(math.radians(tmp.delta), 'U')
            if r == '-':
                tmp.rotate(math.radians(-tmp.delta), 'U')
            if r == '&' or r == '_':
                tmp.rotate(math.radians(tmp.delta), 'L')
            if r == '^':
                tmp.rotate(math.radians(-tmp.delta), 'L')
            if r == '|':
                tmp.rotate(math.radians(tmp.delta), 'H')
            if r == '/':
                tmp.rotate(math.radians(-tmp.delta), 'H')
            if r == '\\':
                tmp.rotate(math.radians(180), 'U')

            if r == '[':
                stack.append((i, copy.deepcopy(tmp)))
            if r == ']':
                i, tmp = stack.pop()

            if r == '@':
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
    def __init__(self, startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color='blue', width=2, tag='fractal'):
        super(FractalGenerate, self).__init__()

        self.params = Params(startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color, width)
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
        newRule = []
        for r in axiom:
            if r in rules:
                newRule.append(rules[r])
            else:
                newRule.append(r)

        return ''.join(newRule)




# def calculate2(self, showInRealTime=False, showSteps=True, field=None):
    #     print('---')
    #     tmpParams = self.params
    #     stack = []
    #     x, y, z, alpha = self.params.x, self.params.y, self.params.z, self.params.alpha
    #
    #     vertex = [(x, y, z)]
    #     links = []
    #
    #     i = 1
    #     j = 2
    #     for r in self.params.axiom:
    #         if r.isalpha():
    #             newX = x + tmpParams.step * math.cos(math.radians(alpha))
    #             newY = y + tmpParams.step * math.sin(math.radians(alpha))
    #             print(int(x), int(y), alpha)
    #             newZ = self.params.z
    #
    #             if r.isupper():
    #                 if showInRealTime:
    #                     seg = Segment_2d(Vector_3d(x, y, z), Vector_3d(newX, newY, newZ),
    #                                      color=tmpParams.color,
    #                                      width=tmpParams.width, tag=self.tag)
    #                     seg.show(field)
    #                     self.segments.append(seg)
    #
    #                     if showSteps:
    #                         field.update()
    #
    #                 vertex.append((newX, newY, newZ))
    #                 links += [i, j]
    #                 self.paramsSegments[f'{i}, {j}'] = (tmpParams.color, tmpParams.width)
    #                 i = j
    #                 j += 1
    #
    #             x, y, z = newX, newY, newZ
    #
    #         if r == '+':
    #             alpha += tmpParams.delta
    #         if r == '-':
    #             alpha -= tmpParams.delta
    #         if r == '[':
    #             stack.append((x, y, z, i, alpha, tmpParams.getCopy()))
    #         if r == ']':
    #             x, y, z, i, alpha, tmpParams = stack.pop()
    #         if r == '@':
    #             tmpParams.width = tmpParams.width * 0.8
    #             tmpParams.step = tmpParams.step * 0.8
    #
    #     if not showSteps and showInRealTime:
    #         field.update()
    #
    #
    #     self.fillVert(vertex)
    #     self.fillPol(links)
