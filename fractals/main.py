from view.RootWithVersions import *
from view.CanvasField import *
from view.keyInput import *
from view.menu import *
from controll.filesWork import *
from model.Fractal import *



def interpret(field, startX=0, startY=0, startAlpha=90, delta=22.5, d=2, axiom='F',
              rules={}, n=5, color='blue', width=2, needClean=True, needDelay=False):

    newFractal = Fractal(startX, startY, startAlpha, delta, d, axiom, rules, n, color, width)
    newFractal.show(field, needClean)

    field.canva.addPol(newFractal)

    if needDelay:
        time.sleep(1)


def drawFractal(field, startParams, fractalParams, colorsParams):
    x, y, alpha = map(int, startParams.getXY())
    Axiom, Rule, Step, Delta, N = fractalParams.getXY()
    Step, Delta = map(float, (Step, Delta))
    rules = eval('{' + Rule + '}')
    N = int(N)

    bg, line, width = colorsParams.getXY()
    try:
        field.canva['bg'] = bg
        field.canva.clear()
        interpret(field, x, y, alpha, Delta, Step, Axiom, rules, N, color=line, width=width)
    except:
        showinfo('Error', 'Неверные параметры')

def main():
    root = RootWithVersions()
    root.geometry('850x650')

    root['bg'] = Settings.COLOR_MAIN_BG

    root.iconphoto(True, PhotoImage(file=r'shared/a1.png'))
    root.title('Фракталы недорого')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0)

    menu = menuFrame(root)
    root.config(menu=menu.create(c, funcReturn=root.loadVersion))
    root.setSaveObjs(c)

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    settings = LabelFrame(root, bg=Settings.COLOR_LOC_LINE)
    settFlag = False

    closeBtn = Button(settings, text="❌", command=lambda: showSettings(), bg=Settings.COLOR_LOC_LINE, bd=0, fg='white')
    closeBtn.place(height=20, width=20, relx=0.89)

    startParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Initial conditions", Settings.WIDTH_INPUT + 3,
                          fields=['X: ', 'Y: ', 'α: '], showButton=False)
    startParams.insertXY((0, 0, 90))
    startParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=10)

    fractalParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Fractal parameters", Settings.WIDTH_INPUT - 2,
                             fields=['Axiom: ', 'Rule: ', 'Step: ', 'Delta: ', 'N: '], showButton=False)
    fractalParams.insertXY(('F-F-F-F', '"F": "FF-F-F-F-FF"', 2, 90, 4))
    fractalParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=160)

    colorsParams = Xs_Ys_Form(settings, Settings.COLOR_LOC_LINE, "Appearance", Settings.WIDTH_INPUT - 2,
                               fields=['Bg: ', 'Line: ', 'Width: '], showButton=False)
    colorsParams.insertXY(('white', 'blue', 2))
    colorsParams.show(Settings.COLOR_LOC_LINE, posx=10, posy=370)

    loadButton = Button(settings, text="Load", padx=21, pady=7, bg="#d1d6e4", command=lambda : loadData(startParams, fractalParams, colorsParams))
    loadButton.place(x=10, y=520)

    saveButton = Button(settings, text="Save", padx=21, pady=7, bg="#d1d6e4", command=lambda : saveData(startParams, fractalParams, colorsParams))
    saveButton.place(x=100, y=520)

    goButton = Button(settings, text="[ Draw fractal ]", padx=40, pady=15, bg=Settings.COLOR_LOC_BG, command=lambda : drawFractal(c, startParams, fractalParams, colorsParams))
    goButton.place(x=10, y=576)

    openBtn = Button(root, text=".\n.\n.", padx=10, pady=10, command=lambda : showSettings(), bg=Settings.COLOR_LOC_BG)
    openBtn.place(x=0, y=0, relheight=1)

    def showSettings():
        nonlocal settFlag
        settFlag = not settFlag
        if settFlag:
            settings.place(x=0, y=0, relheight=1, width=198)
            openBtn.place_forget()
        else:
            settings.place_forget()
            openBtn.place(x=0, y=0, relheight=1)

    root.mainloop()


if __name__ == "__main__":
    main()



