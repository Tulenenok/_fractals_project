from model.BaseObj import BaseObj
import math


class Point(BaseObj):
    def __init__(self, x, y, **params):
        super(Point, self).__init__(**params)

        self.x = x
        self.y = y

    def rotate(self, pointCenter, alpha, mode='gr', side='right'):
        if mode == 'gr':
            alpha = math.radians(alpha)
        if mode == 'right':
            alpha = -alpha

        evk_x = self.x - pointCenter.x
        evk_y = self.y - pointCenter.y
        rotate_evk_x = evk_x * math.cos(alpha) - evk_y * math.sin(alpha)
        rotate_evk_y = evk_x * math.sin(alpha) + evk_y * math.cos(alpha)
        self.x = rotate_evk_x + pointCenter.x
        self.y = rotate_evk_y + pointCenter.y

    def shift(self, xShift, yShift):
        self.x += xShift
        self.y += yShift

    def scale(self, x, y, kx, ky):
        self.x -= x
        self.y -= y
        self.x *= kx
        self.y *= ky
        self.x += x
        self.y += y

    @staticmethod
    def isPointsEqual(pointA, pointB):
        return pointA.x == pointB.x and pointA.y == pointB.y

    @staticmethod
    def dist(pointA, pointB):
        return math.sqrt(pow(pointA.x - pointB.x, 2) + pow(pointA.y - pointB.y, 2))



class Point_2d(Point):
    def __init__(self, x, y, color='black',
                 fontText=('Arial', 8, 'bold'), colorText='black',
                 showComments=False, tag='point'):
        super().__init__(x, y)

        self.color = color
        self.fontText = fontText
        self.colorText = colorText

        self.p, self.t, self.r = None, None, 2

        self.ShowComments = showComments
        self.tag = tag

    def show(self, field, **params):
        x, y = self._coordShift(field)

        self.p = field.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color, outline=self.color, tag=self.tag)
        if self.ShowComments:
            self.t = field.create_text(x + 12, y - 12, text='%.1f; %.1f' % (self.x, self.y), font=self.fontText,
                                       fill=self.colorText, tag=self.tag)

    def hide(self, field, **params):
        if self.p:
            field.delete(self.p)
        if self.t:
            field.delete(self.t)
        self.p, self.t = None, None

    def changeR(self, field):
        self.r = 0
        self.reShow(field)

    def changeColor(self, newColor):
        self.color = newColor

    def isClick(self, field, XEvent, YEvent):
        x, y = self._coordShift(field)
        return x - 4 <= XEvent <= x + 4 and y - 4 <= YEvent <= y + 4

    def _coordShift(self, field):
        try:                                       # Такого метода у канвы может не оказаться
            x, y = field.coordinateShift_2d(self)
        except:
            x, y = self.x, self.y
            print("Вы не переводите координаты точки в координаты канвы, могут быть ошибки")

        return x, y


class Point_3d(Point_2d):
    def __init__(self, x, y, z=0, **params):
        super().__init__(x, y, **params)

        self.z = z


class Pixel(Point_2d):
    def __init__(self, **kwargs):
        super(Pixel, self).__init__(**kwargs)
        self.r = 2

    def show(self, field, **params):
        self.p = field.create_polygon([self.x, self.y], [self.x, self.y + 1], [self.x + 1, self.y + 1], [self.x + 1, self.y], fill=self.color)
        # self.p = field.create_oval(self.x - self.r, self.y - self.r,self.x + self.r, self.y + self.r,
        #                            fill=self.color, outline=self.color)

    def showLikePoint(self, field):
        self.p = field.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color, outline=self.color)