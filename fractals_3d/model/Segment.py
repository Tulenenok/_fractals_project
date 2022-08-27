from model.BaseObj import *
from model.Point import *


class Segment(BaseObj):
    def __init__(self, pointA: Point, pointB: Point, **params):
        super().__init__(**params)

        self.A = pointA.y - pointB.y
        self.B = pointB.x - pointA.x
        self.C = pointA.x * pointB.y - pointA.y * pointB.x

        self.start = pointA                                    # Сохраним две точки, принадлежащие прямой
        self.end = pointB                                      # для дальшейших рассчетов

    def findYByX(self, x):
        return (-self.C - self.A * x) / self.B

    def findXByY(self, y):
        return (-self.C - self.B * y) / self.A


class Segment_2d(Segment):
    def __init__(self, pointA, pointB, color='black', width=2, dash=(100, 2), arrow=None, tag='segment'):
        super().__init__(pointA, pointB)

        self.color = color
        self.width = width
        self.dash = dash
        self.arrow = arrow

        self.l = None

        self.ShowComments = True
        self.needDash = False

        self.xStart, self.yStart = None, None
        self.xEnd, self.yEnd = None, None
        self.tag = tag

    def show(self, field, **params):
        self._coordShift(field)

        xS, yS, xE, yE, = self.xStart, self.yStart, self.xEnd, self.yEnd

        if self.dash and self.needDash:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash, tag=self.tag)
        else:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, tag=self.tag)

    def hide(self, field, **params):
        field.delete(self.l)
        self.l = None

    def _coordShift(self, field):
        self.xStart, self.yStart = field.coordinateShift_2d(self.start)
        self.xEnd, self.yEnd = field.coordinateShift_2d(self.end)


class Line_2d(Segment_2d):
    def __init__(self, pointA, pointB, color='black', width=2, dash=(100, 2), arrow=None, tag='segment'):
        super().__init__(pointA, pointB, color, width, dash, arrow, tag)

    def show(self, field, **params):
        self._coordShift(field)

        xS, yS, xE, yE = 0, 0, 0, 0      # Точки на канве, по которым будем рисовать
        if self.start.x == self.end.x and self.start.y == self.end.y:
            print("Нельзя строить линию по одной точке")
            return

        # Если линия вертикальная, то нужно поменять y от начала координатной сетки до конца
        elif self.start.x == self.end.x:
            xS, yS, xE, yE = self.xStart, 0, self.xStart, field.height

        # Если линия горизонтальная, то нужно поменять x от начала координатной сетки до конца
        elif self.start.y == self.end.y:
            xS, yS, xE, yE = 0, self.yStart, field.width, self.yStart

        # Линия наклонная, надо посчитать для нее координаты от самого левого края, до самого правого
        else:
            helpLine = Segment(Point_2d(self.xStart, self.yStart), Point_2d(self.xEnd, self.yEnd))   # Прямая с коэффициентами канвы
            xS, yS = 0, helpLine.findYByX(0)
            xE, yE = field.width, helpLine.findYByX(field.width)

        if self.dash and self.arrow:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash, arrow=self.arrow, tag=self.tag)
        elif self.dash:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash, tag=self.tag)
        elif self.arrow:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, arrow=self.arrow, tag=self.tag)
        else:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, tag=self.tag)
