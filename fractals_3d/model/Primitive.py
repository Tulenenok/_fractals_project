from model.Pivot import *
from model.Camera import *
from model.Segment import *


class Primitive(BaseObj):
    def __init__(self, color='blue', colorP='magenta', tag='pr', width=2):
        super(Primitive, self).__init__()

        self.localVertices = []     # Локальные вершины (Vector)
        self.globalVertices = []    # Глобальные вершины (Vector)
        self.polygons = []          # Кортежи связей между вершинами (1, 5, 2)...
        self.pivot = Pivot(color=colorP, tag=tag)        # Локальный базис фигуры

        self.color = color
        self.width = width
        self.tag = tag
        self.paramsSegments = dict()
        self._needCalc = True
        self.segments = []

    def move(self, vector):
        self.pivot.move(vector)

        # for i, v in enumerate(self.localVertices):
        #     self.localVertices[i] += vector

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

        self._needCalc = True

    def rotate(self, angle, axis):
        self.pivot.rotate(angle, axis)

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

        self._needCalc = True

    def scale(self, x, y, z):
        for i, v in enumerate(self.localVertices):
            self.localVertices[i].x *= x
            self.localVertices[i].y *= y
            self.localVertices[i].z *= z

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

        self._needCalc = True

    def show(self, field, camera=None):
        # self.pivot.show(field, camera)

        if not camera:
            camera = Camera((0, 0, -400), 100, field)

        for i in range(0, len(self.polygons), 2):
            i1 = self.polygons[i] - 1
            i2 = self.polygons[i + 1] - 1

            v1 = self.globalVertices[i1]
            v2 = self.globalVertices[i2]

            p1 = camera.ScreenProection(v1)
            p2 = camera.ScreenProection(v2)

            key = f'{i1 + 1}, {i2 + 1}'
            params = self.paramsSegments[key] \
                       if key in self.paramsSegments \
                       else (self.color, self.width)
            c, w = params[0], params[1]

            if p1.x is not None and p2.y is not None:
                s1 = Segment_2d(p1, p2, color=c, width=w, tag=self.tag)
                s1.show(field)
                self.segments.append(s1)

        self._needCalc = False

    def hide(self, field, **params):
        self.pivot.hide(field)
        for s in self.segments:
            s.hide(field, **params)
        self.segments.clear()

    def reShow(self, field, camera=None):
        if self._needCalc:
            self.hide(field)
            self.show(field, camera)
        else:
            for s in self.segments:
                s.reShow(field)