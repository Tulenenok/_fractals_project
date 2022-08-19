import math
import pickle
import random
from tkinter.messagebox import showinfo
import tkinter as tk

from PIL import ImageTk, Image

from view.CanvasPoint import CanvasPoint
from view.CanvasLine import CanvasLine
from view.Settings import Settings
from view.CanvasPolygon import *
#from view.keyInput import *

from model.Tools import Tools

from tkinter import *
from tkinter.colorchooser import askcolor


# пример создания  ResizingCanvas(myFrame, width=850, height=400, bg="red", highlightthickness=0)
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.resize)

        self.bind('<1>', lambda event: self.click(event), '+')
        self.bind("<Motion>", lambda event: self.showCoords(event), '+')
        self.bind("<Leave>", lambda event: self.hideCoords(event), '+')

        self.bind("<MouseWheel>", self.mouseZoom, '+')

        self.bind("<Shift-Down>", lambda event: self.shift(0, 10), '+')
        self.bind("<Shift-Left>", lambda event: self.shift(-10, 0), '+')
        self.bind("<Shift-Up>", lambda event: self.shift(0, -10), '+')
        self.bind("<Shift-Right>", lambda event: self.shift(10, 0), '+')

        self.height = self.winfo_height()
        self.width = self.winfo_width()

        self.image = None

        self.needRebuild = False

    def mouseRotate(self, mode):
        pass

    def shift(self, xShift, yShift):
        pass

    def addImage(self):
        image = ImageTk.PhotoImage(file=r"/shared/rootIcon4.png")
        self.image = self.create_image(10, 10, image=image, anchor=NW)

    def resize(self, event):
        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)
        self.needRebuild = True

    def click(self, event):
        print('click')

    def showCoords(self, event):
        pass

    def hideCoords(self, event):
        pass

    def mouseZoom(self, event):
        pass

    def plug(self, event):
        print('plus')

    def arrowMoveAcrossField(self, axis, side):
        pass


class CoordGrid(ResizingCanvas):
    def __init__(self, window, XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=True, **kwargs):
        super(CoordGrid, self).__init__(window, **kwargs)
        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd

        self.XLine, self.YLine = None, None
        self.gridLines = []
        self.gridDashes = []
        self.gridText = []

        self.gridCoefX = gridCoef
        self.gridCoefY = gridCoef

        self.showArrows = showArrows

        self.DASH = (3, 3)
        self.COLOR = 'black'

    def changeLimits(self, XStart, XEnd, YStart, YEnd, flagChangeCoef=True):
        if flagChangeCoef:
            if self.controllCoef(XStart, XEnd, YStart, YEnd):
                return Tools.EXIT_FAILURE

        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd
        self.myUpdate()

    def coordinateShift(self, canvasPoint):
        return self.XShiftPC(canvasPoint.x), self.YShiftPC(canvasPoint.y)

    # Перевод координаты X из представления человека в представление канвы
    def XShiftPC(self, x):
        return 0 + (x - self.XStart) * self.width / abs(self.XEnd - self.XStart)

    # Перевод координаты Y из представления человека в представление канвы
    def YShiftPC(self, y):
        return self.height - (y - self.YStart) * self.height / abs(self.YEnd - self.YStart)

    # Перевод координаты X из представления канвы в представление человека
    def XShiftCP(self, x):
        return self.XStart + x * abs(self.XEnd - self.XStart) / self.width

    # Перевод координаты Y из представления канвы в представление человека
    def YShiftCP(self, y):
        return self.YEnd - y * abs(self.YEnd - self.YStart) / self.height

    # Перевод длины отрезка из представления человека в представление канвы
    def XLineShiftPC(self, lenLine):
        return lenLine * self.width / abs(self.XEnd - self.YStart)

    def arrowsShow(self):
        if self.showArrows:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill='black', width=2, arrow=LAST)
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill='black', width=2, arrow=LAST)
        else:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill=self.COLOR, width=1, dash=self.DASH)
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill=self.COLOR, width=1, dash=self.DASH)

    def arrowsHide(self):
        if self.XLine:
            self.delete(self.XLine)
        if self.YLine:
            self.delete(self.YLine)
        self.XLine, self.YLine = None, None

    def arrowsUpdate(self):
        self.arrowsHide()
        self.arrowsShow()

    def gridShow(self):
        # вертикальная сетка (рисуем линии параллельные оси Y)
        step = self.width / 2 / self.gridCoefX
        i = 0
        while i < self.width - step:
            i += step
            if math.fabs(i - self.width / 2) < 1:
                continue

            self.gridLines.append(self.create_line(i, self.height, i, 0, fill=self.COLOR, width=1, dash=self.DASH))
            if self.showArrows:
                self.gridDashes.append(self.create_line(i, self.height / 2 - 4, i, self.height / 2 + 4, fill='black', width=2))
                self.gridText.append(self.create_text(i, self.height / 2 - 12, text=str(int(self.XShiftCP(i))), font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # горизонтальная сетка (рисуем линии параллельные оси X)
        step = self.height / 2 / self.gridCoefY
        i = 0
        while i < self.height - step:
            i += step
            if math.fabs(i - self.height / 2) < 1:
                continue
            self.gridLines.append(self.create_line(0, i, self.width, i, fill=self.COLOR, width=1, dash=self.DASH))
            if self.showArrows:
                self.gridDashes.append(self.create_line(self.width / 2 - 4, i, self.width / 2 + 4, i, fill='black', width=2))
                self.gridText.append(self.create_text(self.width / 2 + 12, i, text=str(int(self.YShiftCP(i))),
                                                        font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # Подпись осей координат
        if self.showArrows:
            self.gridText.append(self.create_text(self.width / 2 + 12, 12, text='Y',
                                                        font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))
            self.gridText.append(self.create_text(self.width - 12, self.height / 2 + 12, text='X',
                                                        font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))

    def gridHide(self):
        for line in self.gridLines:
            self.delete(line)

        for dash in self.gridDashes:
            self.delete(dash)

        for text in self.gridText:
            self.delete(text)

        self.gridLines.clear()
        self.gridDashes.clear()

    def gridUpdate(self):
        self.gridHide()
        self.gridShow()

    def myUpdate(self):
        self.arrowsUpdate()
        self.gridUpdate()

    def resize(self, event):
        super().resize(event)
        self.correct_field()
        self.myUpdate()

    def correct_field(self):
        width = self.winfo_width()
        height = self.winfo_height()

        fwidth = self.XEnd - self.XStart
        fheight = self.YEnd - self.YStart

        fxmid = (self.XEnd + self.XStart) / 2
        new_fwidth = fheight * width / height
        self.XStart = fxmid - new_fwidth / 2
        self.XEnd = fxmid + new_fwidth / 2

        self.changeLimits(self.XStart, self.XEnd, self.YStart, self.YEnd)

    def zoomPlus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX < 1:
            self.gridCoefX -= 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY < 1:
            self.gridCoefY -= 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def zoomMinus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX >= 2 and self.gridCoefX < 10:
            self.gridCoefX += 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY >= 2 and self.gridCoefY < 10:
            self.gridCoefY += 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def arrowMoveAcrossField(self, axis, side):
        if axis == 'X':
            step = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart + (step if side == 'right' else -step),
                              self.XEnd + (step if side == 'right' else -step),
                              self.YStart, self.YEnd)
        else:
            step = abs(self.YStart - self.YEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart, self.XEnd, self.YStart + (step if side == 'up' else -step),
                                     self.YEnd + (step if side == 'up' else -step))

    def controllCoef(self, XStart, XEnd, YStart, YEnd):
        if abs(XEnd - XStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для X')
            return Tools.EXIT_FAILURE

        if abs(YEnd - YStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для Y')
            return Tools.EXIT_FAILURE

        self.zoomPlus(XStart, XEnd, YStart, YEnd)
        self.zoomMinus(XStart, XEnd, YStart, YEnd)

        return Tools.EXIT_SUCCESS

    def mouseZoom(self, event):
        stepX = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
        stepY = abs(self.YStart - self.YEnd) / self.gridCoefY / 2
        if event.delta > 0:
            self.changeLimits(self.XStart + stepX, self.XEnd - stepX, self.YStart + stepY, self.YEnd - stepY, True)
        elif event.delta < 0:
            self.changeLimits(self.XStart - stepX, self.XEnd + stepX, self.YStart - stepY, self.YEnd + stepY, True)

    def changeCoef(self, sign, *axis):
        if sign == '+':
            self.gridCoefX = self.gridCoefX - 1 if 'X' in axis and self.gridCoefX > 1 else self.gridCoefX
            self.gridCoefY = self.gridCoefY - 1 if 'Y' in axis and self.gridCoefY > 1 else self.gridCoefY
        else:
            self.gridCoefX = self.gridCoefX + 1 if 'X' in axis and self.gridCoefX < 10 else self.gridCoefX
            self.gridCoefY = self.gridCoefY + 1 if 'Y' in axis and self.gridCoefY < 10 else self.gridCoefY

        self.myUpdate()

    def flagShowGrid(self, flag):
        self.showArrows = flag
        self.myUpdate()


class CartesianField(CoordGrid):
    def __init__(self, rootFrame, root, colorPoints=Settings.COLOR_LINE,
                 XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=False, **kwargs):
        super(CartesianField, self).__init__(rootFrame, XStart, XEnd, YStart, YEnd, gridCoef, showArrows, **kwargs)
        self.root = root
        self.ShowComments = False

    def myUpdate(self):
        super().myUpdate()
        self.updateShowFlags()

    def clear(self):
        pass

    def save(self):
        try:
            self.root.saveVersion()
        except:
            print('Вы не используете сохранение')

    def saveCanva(self, f):
        self.save()

    def loadCanva(self, f):
        pass

    def updateShowFlags(self):
        pass


class PolygonField(CartesianField):
    def __init__(self, rootFrame, root, **kwargs):
        super(PolygonField, self).__init__(rootFrame, root, **kwargs)

        self.rotatePoint = CanvasPoint(0, 0)
        self.colorNowPol = Settings.COLOR_LINE

        self.polygons = []
        self.binds = []

    def click(self, event):
        pass

    def showPoint(self, x, y, color=Settings.COLOR_NEW_POINT):
        col = self.colorNowPol

        point = CanvasPoint(float(x), float(y), showComments=self.ShowComments, color=col)
        self.polygons[-1].addPoint(self, point, col)

    def createBinds(self):
        pass

    def delBinds(self):
        pass

    def showCoords(self, event):
        super(PolygonField, self).showCoords(event)

    def clear(self):
        self.delete('line')
        self.polygons.clear()

    def clearResult(self):
        self.clear()

    def myUpdate(self):
        super(PolygonField, self).myUpdate()
        for pol in self.polygons:
            pol.reShow(self)

    def addPol(self, pol):
        self.polygons.append(pol)

    def delPol(self, pol):
        try:
            self.polygons.remove(pol)
        except:
            print('Элемент для удаления не найден')

    def saveCanva(self, f):
        pickle.dump(self.polygons, f)

    def loadCanva(self, f):
        try:
            polygons = pickle.load(f)
        except:
            print('Ошибка загрузки полигона')
            return Tools.EXIT_FAILURE

        self.clear()

        self.polygons = polygons
        self.myUpdate()
        return Tools.EXIT_SUCCESS

    def updateShowFlags(self):
        super(PolygonField, self).updateShowFlags()

    def changeColor(self, XEvent, YEvent):
        color = askcolor()[1]
        if not color:
            return

        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    pol.changeColor(color, color)

        self.myUpdate()
        self.save()

    def updatePoints(self):
        self.points = []
        for pol in self.polygons:
            for i in pol.points:
                self.points.append(i)

    def shift(self, xShift, yShift):
        for pol in self.polygons:
            pol.hide(self)
            pol.shiftPol(xShift, yShift)

        self.myUpdate()
        self.save()

    def scale(self, x, y, kx, ky):
        for pol in self.polygons:
            pol.hide(self)
            pol.scalePol(x, y, kx, ky)

        self.myUpdate()
        self.save()

    def mouseRotate(self, mode):
        pass

    def mouseZoom(self, event):
        super(PolygonField, self).mouseZoom(event)


class WrapCanva:
    def __init__(self, window, Canva=PolygonField, **kwargs):
        self.window = window

        self.frame = Frame(window)
        self.canva = Canva(self.frame, self.window, showArrows=False, **kwargs)
        self.canva.config(bg='white')
        self.frame.bind('<Configure>', self.resize, '+')
        self.canva.place(x=0, y=0)

        self.pointMenu = None
        self.Xevent, self.Yevent = None, None
        self.bind()

        image = ImageTk.PhotoImage(file=r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon4.png")
        self.canva.create_image(10, 10, image=image, anchor=NW)

    def bind(self):
        self.window.bind("<Right>", lambda event: self.canva.arrowMoveAcrossField('X', 'right'), '+')
        self.window.bind("<Left>", lambda event: self.canva.arrowMoveAcrossField('X', 'left'), '+')
        self.window.bind("<Up>", lambda event: self.canva.arrowMoveAcrossField('Y', 'up'), '+')
        self.window.bind("<Down>", lambda event: self.canva.arrowMoveAcrossField('Y', 'down'), '+')

        # self.window.bind("<Control-equal>", lambda event: self.canva
        # .changeCoef('+', 'X', 'Y'))
        # self.window.bind("<Control-minus>", lambda event: self.canva.changeCoef('-', 'X', 'Y'))

        self.window.bind("<Control-equal>", lambda event: self.canva.scale(0, 0, 2, 2), '+')
        self.window.bind("<Control-minus>", lambda event: self.canva.scale(0, 0, 0.5, 0.5), '+')

        self.window.bind("<Control-z>", lambda event: self.window.loadVersion(), '+')
        self.window.bind("<Control-s>", lambda event: self.window.loadVersion(), '+')
        self.window.bind("<Control-p>", lambda event: self.canva.mouseRotate('r'), '+')
        self.window.bind("<Control-o>", lambda event: self.canva.mouseRotate('l'), '+')
        self.window.bind("<Control-n>", lambda event: self.changeColorRandom())

        # self.window.bind("<Control-space>", lambda event: self.canva.startNewPolygonClose(event), '+')

        self.pointMenu = Menu(self.canva, tearoff=0)
        # self.pointMenu.add_command(label="Delete", command=lambda: self.canva.rightClick(self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Change color", command=lambda: self.canva.changeColor(self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Set rotate point", command=lambda: self.changeRotatePoint())

        self.mainMenu = Menu(self.canva, tearoff=0)
        self.mainMenu.add_command(label="Set rotate point", command=lambda: self.changeRotatePoint())

        self.window.bind("<Button-3>", lambda event: self.rightClick(event), '+')

    def changeRotatePoint(self):
        x = int(self.canva.XShiftCP(self.Xevent))
        y = int(self.canva.YShiftCP(self.Yevent))

    def action(self, frame):
        z = Toplevel(self.window)
        z.geometry('200x200')
        z.title('')
        z['bg'] = Settings.COLOR_MAIN_BG
        z.resizable(0, 0)
        f = frame(z, 200, 200, self)
        f.show()

    def rightClick(self, event):
        self.Xevent = event.x
        self.Yevent = event.y

        isPointHere = self.canva.isPointInPol(self.Xevent, self.Yevent)

        if isPointHere:
            self.pointMenu.post(event.x_root, event.y_root)
        else:
            self.mainMenu.post(event.x_root, event.y_root)

    def resize(self, event):
        self.canva.resize(event)

    def show(self, x, y, relwidth, relheight):
        self.frame.place(x=x, y=y, relwidth=relwidth, relheight=relheight)

    def clear(self):
        self.canva.clear()

    def getPoints(self):
        return [point for p in self.canva.polygons for point in p.points]

    def getPointsForSave(self):
        return [[point for point in p.points] for p in self.canva.polygons]

    def saveVersion(self, f):
        self.canva.saveCanva(f)

    def loadVersion(self, f):
        return self.canva.loadCanva(f)

    def radioShowComments(self):
        self.canva.ShowComments = not self.canva.ShowComments
        self.canva.myUpdate()

    def changeColorNewPol(self, color=None):
        if not color:
            color = askcolor()[1]
            if not color:
                return

        self.canva.colorNowPol = color

    def changeColorRandom(self):
        newColor = Tools.rgb_to_hex(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.changeColorNewPol(newColor)


    def changeColorDelObl(self):
        color = askcolor()[1]
        if not color:
            return

        Settings.COLOR_NEW_CLIPPER = color

    def changeColorDel(self):
        color = askcolor()[1]
        if not color:
            return

        Settings.COLOR_DEL = color


