from model.Point import Point
from view.Settings import Settings

class CanvasPoint(Point):
    def __init__(self, x, y, color=Settings.COLOR_LINE, fontText=('Arial', 8, 'bold'), colorText='black', showComments=False):
        super().__init__(x, y)
        self.color = color

        self.fontText = fontText
        self.colorText = colorText

        self.p, self.t = None, None

        self.r = 2

        self.ShowComments = showComments

    def changeR(self, field):
        self.r = 0
        self.reShow(field)

    def coordShift(self, field):
        try:                                       # Такого метода у канвы может не оказаться
            x, y = field.coordinateShift(self)
        except:
            x, y = self.x, self.y
            print("Вы не переводите координаты точки в координаты канвы, могут быть ошибки")

        return x, y

    def show(self, field):
        x, y = self.coordShift(field)

        self.p = field.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color, outline=self.color)
        if self.ShowComments:
            self.t = field.create_text(x + 12, y - 12, text='%.1f; %.1f' % (self.x, self.y), font=self.fontText,
                                       fill=self.colorText)


    def hide(self, field):
        if self.p:
            field.delete(self.p)
        if self.t:
            field.delete(self.t)
        self.p, self.t = None, None

    def changeColor(self, newColor):
        self.color = newColor

    def reShow(self, canva):
        self.hide(canva)
        self.show(canva)

    def isClick(self, field, XEvent, YEvent):
        try:                                       # Такого метода у канвы может не оказаться
            x, y = field.coordinateShift(self)
        except:
            x, y = self.x, self.y
            print("Вы не переводите координаты точки в координаты канвы, могут быть ошибки")

        if x - 4 <= XEvent <= x + 4 and y - 4 <= YEvent <= y + 4:
            return True

        return False

    def highlight(self, field):
        pass
        # self.r = 5

    def hideHightlight(self, field):
        pass
        # self.r = 2


class Pixel(CanvasPoint):
    def __init__(self, **kwargs):
        super(Pixel, self).__init__(**kwargs)
        self.r = 2

    def show(self, field):
        self.p = field.create_polygon([self.x, self.y], [self.x, self.y + 1], [self.x + 1, self.y + 1], [self.x + 1, self.y], fill=self.color)
        # self.p = field.create_oval(self.x - self.r, self.y - self.r,self.x + self.r, self.y + self.r,
        #                            fill=self.color, outline=self.color)

    def showLikePoint(self, field):
        self.p = field.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color, outline=self.color)


