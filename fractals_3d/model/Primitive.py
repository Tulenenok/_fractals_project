from model.Pivot import *
from model.Camera import *
from model.Segment import *


class Primitive(BaseObj):
    def __init__(self, color='blue', colorP='magenta', tag='pr'):
        super(Primitive, self).__init__()

        self.localVertices = []     # Локальные вершины (Vector)
        self.globalVertices = []    # Глобальные вершины (Vector)
        self.polygons = []          # Кортежи связей между вершинами (1, 5, 2)...
        self.pivot = Pivot(color=colorP, tag=tag)        # Локальный базис фигуры

        self.color = color
        self.tag = tag
        self.segments = []

    def move(self, vector):
        self.pivot.move(vector)

        # for i, v in enumerate(self.localVertices):
        #     self.localVertices[i] += vector

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

    def rotate(self, angle, axis):
        self.pivot.rotate(angle, axis)

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

    def scale(self, x, y, z):
        for i, v in enumerate(self.localVertices):
            self.localVertices[i].x *= x
            self.localVertices[i].y *= y
            self.localVertices[i].z *= z

        for i, v in enumerate(self.localVertices):
            self.globalVertices[i] = self.pivot.toGlobalCoords(self.localVertices[i])

    def show(self, field, camera=None):
        self.pivot.show(field, camera)

        if not camera:
            camera = Camera((0, 0, -400), 200, field)

        for i in range(0, len(self.polygons), 2):
            i1 = self.polygons[i] - 1
            i2 = self.polygons[i + 1] - 1

            v1 = self.globalVertices[i1]
            v2 = self.globalVertices[i2]

            # p1 = camera.ScreenProection(v1)
            # p2 = camera.ScreenProection(v2)

            p1 = Point_2d(v1.x, v1.y)
            p2 = Point_2d(v2.x, v2.y)

            s1 = Segment_2d(p1, p2, color=self.color, tag=self.tag)
            s1.show(field)
            self.segments.append(s1)

    def hide(self, field, **params):
        self.pivot.hide(field)
        for s in self.segments:
            s.hide(field, **params)
        self.segments.clear()

    def reShow(self, field, camera=None):
        self.hide(field)
        field.update()
        self.show(field, camera)
