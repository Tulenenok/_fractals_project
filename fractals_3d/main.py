from model.Vector import Vector_3d
from view.RootWithVersions import *
from view.Field import *
from view.InputForm import *
from view.Menu import *
from controll.FileWork import *
from model.Fracral import *
import time


def interpret(field, startX=0, startY=0, startZ=0, startAlpha=90, delta=22.5, d=2, axiom='F',
              rules={}, n=5, color='blue', width=2, needClean=True, needDelay=False, constants=[]):

    newFractal = FractalGenerate(startX, startY, startZ, startAlpha, delta, d, axiom, rules, n, color, width, constants=constants)
    newFractal.show(field, needClean)

    field.canva.addPol(newFractal.lastFractal)

    if needDelay:
        time.sleep(1)


def drawFractal(field, startParams, fractalParams, colorsParams):
    x, y, z, alpha = startParams.getXY()
    Axiom, Rule, Step, Delta, N, constants = fractalParams.getXY()
    Rule = Rule.replace("\\", "|")
    Rule = Rule.replace("||", "|")
    bg, line, width = colorsParams.getXY()

    field.canva['bg'] = bg
    field.canva.clear()
    interpret(field, x, y, z, alpha, Delta, Step, Axiom, Rule, N, color=line, width=width, constants=constants)

    # try:
    #     field.canva['bg'] = bg
    #     field.canva.clear()
    #     interpret(field, x, y, alpha, Delta, Step, Axiom, Rule, N, color=line, width=width)
    # except:
    #     showinfo('Error', 'Неверные параметры')


def main():
    root = RootWithVersions()
    root.geometry('850x650')

    root['bg'] = Settings.COLOR_MAIN_BG

    root.iconphoto(True, PhotoImage(file=r'data/a1.png'))
    root.title('Фракталы недорого')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0)

    menu = menuFrame(root)
    root.config(menu=menu.create(c, funcReturn=root.loadVersion))
    root.setSaveObjs(c)

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    settings = LabelFrame(root, bg=Settings.COLOR_LOC_LINE)
    settFlag = False

    # settings
    closeBtn = Button(settings, text="❌", command=lambda: showSettings(), bg=Settings.COLOR_LOC_LINE, bd=0, fg='white')
    closeBtn.place(height=20, width=20, relx=0.89)

    startParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Initial conditions", Settings.WIDTH_INPUT + 3,
                          fields=['X: ', 'Y: ', 'Z', 'α: '], showButton=False)
    startParams.insertXY((0, 0, 0, 90))
    startParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=10)

    fractalParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Fractal parameters", Settings.WIDTH_INPUT - 2,
                             fields=['Axiom: ', 'Rule: ', 'Step: ', 'Delta: ', 'N: ', 'Const: '], showButton=False)
    # fractalParams.insertXY(('F-F-F-F', "['F: FF-F-F-F-FF']", 2, 90, 4))

    fractalParams.insertXY(('F(1, 2)', "['F(x): F(x)-F(x)-F(x)-F(x)', 'F(x, y): F(x)-F(x)-F(x)-F(x)']", 2, 90, 4, []))

    fractalParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=160)

    colorsParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Appearance", Settings.WIDTH_INPUT - 2,
                               fields=['Bg: ', 'Line: ', 'Width: '], showButton=False)
    colorsParams.insertXY(('white', 'blue', 2))
    colorsParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=370)

    loadButton = Button(settings, text="Load", padx=21, pady=7, bg="#d1d6e4", command=lambda : FileWork.loadData(startParams, fractalParams, colorsParams))
    loadButton.place(x=10, y=520)

    saveButton = Button(settings, text="Save", padx=21, pady=7, bg="#d1d6e4", command=lambda : FileWork.saveData(startParams, fractalParams, colorsParams))
    saveButton.place(x=100, y=520)

    goButton = Button(settings, text="[ Draw fractal ]", padx=40, pady=15, bg=Settings.COLOR_LOC_BG, command=lambda : drawFractal(c, startParams, fractalParams, colorsParams))
    goButton.place(x=10, y=576)
    # settings

    openBtn = Button(root, text="🌷", padx=6, pady=10, command=lambda : showSettings(), bg=Settings.COLOR_LOC_BG)
    openBtn.place(x=0, rely=0, relheight=0.5)

    def showSettings(param=1):
        nonlocal settFlag
        settFlag = not settFlag
        if settFlag:
            openBtn.place_forget()
            openBtn2.place_forget()
            if param == 1:
                settings.place(x=0, y=0, relheight=1, width=198)
            else:
                settings2.place(x=0, y=0, relheight=1, width=198)
        else:
            if param == 1:
                settings.place_forget()
            else:
                settings2.place_forget()
            openBtn.place(x=0, rely=0, relheight=0.5)
            openBtn2.place(x=0, rely=0.5, relheight=0.5)


    #setting2
    settings2 = LabelFrame(root, bg=Settings.COLOR_LOC_LINE)
    settFlag = False

    closeBtn2 = Button(settings2, text="❌", command=lambda: showSettings(2), bg=Settings.COLOR_LOC_LINE, bd=0,
                       fg='white')
    closeBtn2.place(height=20, width=20, relx=0.89)

    rotateParams = Xs_Ys_Form(settings2, Settings.COLOR_LOC_LINE, "Rotate", Settings.WIDTH_INPUT + 2,
                              fields=['x°: ', 'y°: ', 'z°: '], showButton=True, btnText='rotate',
                              command=lambda: figureWork('rotate', '1'))
    rotateParams.insertXY((10, 10, 10))
    rotateParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=2)

    moveParams = Xs_Ys_Form(settings2, Settings.COLOR_LOC_LINE, "Move", Settings.WIDTH_INPUT + 2,
                            fields=['dx: ', 'dy: ', 'dz: '], showButton=True, btnText='move',
                            command=lambda: figureWork('move', '1'))
    moveParams.insertXY((10, 10, 10))
    moveParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=175)

    scaleParams = Xs_Ys_Form(settings2, Settings.COLOR_LOC_LINE, "Scale", Settings.WIDTH_INPUT + 2,
                             fields=['kx: ', 'ky', 'kz'], showButton=True, btnText='scale',
                             command=lambda: figureWork('scale', '1'))
    scaleParams.insertXY((2, 2, 2))
    scaleParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=340)

    goButton2 = Button(settings2, text="[ Load figure ]", padx=40, pady=15, bg=Settings.COLOR_LOC_BG,
                      command=lambda: figureWork('load', '1'))
    goButton2.place(x=10, y=576)
    # settings2

    openBtn2 = Button(root, text=".\n.\n.\n", padx=10, pady=10, command=lambda: showSettings(2), bg=Settings.COLOR_LOC_BG)
    openBtn2.place(x=0, rely=0.5, relheight=0.5)

    fig = None

    def figureWork(mode, param):
        nonlocal fig
        if mode == 'load':
            if fig:
                fig.hide(c.canva)

            fig = FileWork.loadFigure()
            c.canva.addPol(fig)
        elif mode == 'rotate':
            x, y, z = map(math.radians, map(float, rotateParams.getXY()))
            c.canva.rotate(x, 'x')
            c.canva.rotate(y, 'y')
            c.canva.rotate(z, 'z')
        elif mode == 'move':
            x, y, z = map(float, moveParams.getXY())
            c.canva.move(Vector_3d(x, y, z))
        elif mode == 'scale':
            x, y, z = map(float, scaleParams.getXY())
            c.canva.scale(x, y, z)

        if fig:
            fig.reShow(c.canva)

    root.mainloop()


if __name__ == "__main__":
    main()



