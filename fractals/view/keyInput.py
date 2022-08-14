from tkinter import *
from tkinter.messagebox import *
from model.Tools import Tools
from view.Settings import Settings
# from view.Btn import WrapButton
from view.CanvasPoint import CanvasPoint


class XForm:
    def __init__(self, root, color, text, widthEntry, command, btnText, padx=5, pady=10, width=10,
                 font=('Arial', 11, 'bold'), fg="#f1e4de", fields="OX: ", showButton=True):
        self.f = LabelFrame(root, bg=color, text=text, padx=padx, pady=pady, width=width, font=font, fg=fg)
        self.xEntry = Entry(self.f, width=widthEntry)
        self.btn = Button(self.f, text=btnText, command=command)

        self.btn.bind("<Enter>", self.onEnter)
        self.btn.bind("<Leave>", self.onLeave)
        self.showButton = showButton

        if self.showButton:
            self.xEntry.bind("<Return>", lambda event: command())

        self.fg = fg

        self.fields=fields

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def show(self, color, posx=10, poxy=10):
        self.f.propagate(0)

        Label(self.f, text=self.fields, bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=0)
        self.xEntry.grid(row=0, column=1, sticky=W)

        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=1)
        self.btn.grid(row=2, column=1, sticky="es")

        self.f.place(x=posx, y=poxy)

    def clear(self):
        self.xEntry.delete(0, END)
        self.xEntry.focus_set()

    def getXY(self):
        return self.xEntry.get()

    def insertXY(self, x):
        self.xEntry.delete(0, END)
        self.xEntry.insert(0, str(x))


class XYForm:
    def __init__(self, root, color, text, widthEntry, command, btnText, padx=5, pady=10, width=10,
                 font=('Arial', 11, 'bold'), fg="#f1e4de"):
        self.f = LabelFrame(root, bg=color, text=text, padx=padx, pady=pady, width=width, font=font, fg=fg)
        self.xEntry = Entry(self.f, width=widthEntry)
        self.yEntry = Entry(self.f, width=widthEntry)
        self.btn = Button(self.f, text=btnText, command=command)

        self.btn.bind("<Enter>", self.onEnter)
        self.btn.bind("<Leave>", self.onLeave)

        self.xEntry.bind("<Return>", lambda event: self.yEntry.focus_set())
        self.yEntry.bind("<Return>", lambda event: command())

        self.xEntry.bind("<Down>", lambda event: self.yEntry.focus_set())
        self.yEntry.bind("<Up>", lambda event: self.xEntry.focus_set())

        self.fg = fg

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def show(self, color, posx=10, poxy=10):
        self.f.propagate(0)

        Label(self.f, text="X: ", bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=0)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=1)
        Label(self.f, text="Y: ", bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=2)

        self.xEntry.grid(row=0, column=1, sticky=W)
        self.yEntry.grid(row=2, column=1, sticky=W)

        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=3)
        self.btn.grid(row=4, column=1, sticky="es")

        # self.f.pack(side=packSide, anchor=packAnchor)
        self.f.place(x=posx, y=poxy)

    def clear(self):
        self.xEntry.delete(0, END)
        self.yEntry.delete(0, END)
        self.xEntry.focus_set()

    def getXY(self):
        return self.xEntry.get(), self.yEntry.get()



class XYXForm:
    def __init__(self, root, color, text, widthEntry=2, command=None, btnText="btn", padx=5, pady=10, width=10,
                 font=('Arial', 11, 'bold'), fg="black", showButton=True, fields=["Start: ", "End: ", "Step: "]):
        self.showButton = showButton

        self.f = LabelFrame(root, bg=color, text=text, padx=padx, pady=pady, width=width, font=font, fg=fg)
        self.x1Entry = Entry(self.f, width=widthEntry)
        self.y1Entry = Entry(self.f, width=widthEntry)
        self.x2Entry = Entry(self.f, width=widthEntry)
        self.btn = Button(self.f, text=btnText, command=command)

        self.fg = fg

        self.bind(command)

        self.fields = fields

    def insertXY(self, x1, y1, x2):
        self.x1Entry.delete(0, END)
        self.y1Entry.delete(0, END)
        self.x2Entry.delete(0, END)
        self.x1Entry.insert(0, str(x1))
        self.y1Entry.insert(0, str(y1))
        self.x2Entry.insert(0, str(x2))

    def bind(self, command):
        self.btn.bind("<Enter>", self.onEnter)
        self.btn.bind("<Leave>", self.onLeave)

        self.x1Entry.bind("<Return>", lambda event: self.y1Entry.focus_set())
        self.y1Entry.bind("<Return>", lambda event: self.x2Entry.focus_set())
        if self.showButton:
            self.x2Entry.bind("<Return>", lambda event: command())

        self.x1Entry.bind("<Down>", lambda event: self.y1Entry.focus_set())
        self.y1Entry.bind("<Up>", lambda event: self.x1Entry.focus_set())
        self.y1Entry.bind("<Down>", lambda event: self.x2Entry.focus_set())
        self.x2Entry.bind("<Up>", lambda event: self.y1Entry.focus_set())

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def show(self, color, posx=10, posy=10):
        self.f.propagate(0)

        Label(self.f, text=self.fields[0], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=0)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=1)
        Label(self.f, text=self.fields[1], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=2)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=3)
        Label(self.f, text=self.fields[2], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=4)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=5)

        self.x1Entry.grid(row=0, column=1, sticky=W)
        self.y1Entry.grid(row=2, column=1, sticky=W)
        self.x2Entry.grid(row=4, column=1, sticky=W)

        if self.showButton:
            Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg="#f1e4de").grid(row=7)
            self.btn.grid(row=8, column=1, sticky="es")

        self.f.place(x=posx, y=posy)

    def clear(self):
        self.x1Entry.delete(0, END)
        self.y1Entry.delete(0, END)
        self.x2Entry.delete(0, END)
        self.x1Entry.focus_set()

    def getXY(self):
        return self.x1Entry.get(), self.y1Entry.get(), self.x2Entry.get()


class XYXBtnForm:
    def __init__(self, root, color, text, widthEntry, command, btnText, padx=5, pady=10, width=10,
                 font=('Arial', 11, 'bold'), fg="#f1e4de", showButton=True, fields=["OX: ", "OY: ", "OZ: "]):
        self.showButton = showButton

        self.f = LabelFrame(root, bg=color, text=text, padx=padx, pady=pady, width=width, font=font, fg=fg)
        self.x1Entry = Entry(self.f, width=widthEntry)
        self.y1Entry = Entry(self.f, width=widthEntry)
        self.x2Entry = Entry(self.f, width=widthEntry)

        self.btn1 = Button(self.f, text=btnText, command=command)
        self.btn2 = Button(self.f, text=btnText, command=command)
        self.btn3 = Button(self.f, text=btnText, command=command)

        self.fg = fg

        self.bind(command)

        self.fields = fields

    def insertXY(self, x1, y1, x2):
        self.x1Entry.delete(0, END)
        self.y1Entry.delete(0, END)
        self.x2Entry.delete(0, END)
        self.x1Entry.insert(0, str(x1))
        self.y1Entry.insert(0, str(y1))
        self.x2Entry.insert(0, str(x2))

    def bind(self, command):
        self.btn1.bind("<Enter>", self.onEnter)
        self.btn1.bind("<Leave>", self.onLeave)
        self.btn2.bind("<Enter>", self.onEnter)
        self.btn2.bind("<Leave>", self.onLeave)
        self.btn3.bind("<Enter>", self.onEnter)
        self.btn3.bind("<Leave>", self.onLeave)

        self.x1Entry.bind("<Return>", lambda event: self.y1Entry.focus_set())
        self.y1Entry.bind("<Return>", lambda event: self.x2Entry.focus_set())
        if self.showButton:
            self.x2Entry.bind("<Return>", lambda event: command())

        self.x1Entry.bind("<Down>", lambda event: self.y1Entry.focus_set())
        self.y1Entry.bind("<Up>", lambda event: self.x1Entry.focus_set())
        self.y1Entry.bind("<Down>", lambda event: self.x2Entry.focus_set())
        self.x2Entry.bind("<Up>", lambda event: self.y1Entry.focus_set())

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def show(self, color, posx=10, poxy=10):
        self.f.propagate(0)

        Label(self.f, text=self.fields[0], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=0)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=1)
        Label(self.f, text=self.fields[1], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=2)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=3)
        Label(self.f, text=self.fields[2], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=4)
        Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=5)

        self.x1Entry.grid(row=0, column=1, sticky=W)
        self.y1Entry.grid(row=2, column=1, sticky=W)
        self.x2Entry.grid(row=4, column=1, sticky=W)

        # Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg="#f1e4de").grid(row=7)
        if self.showButton:
            self.btn1.grid(row=0, column=2, sticky="es")
            self.btn2.grid(row=1, column=2, sticky="es")
            self.btn3.grid(row=2, column=2, sticky="es")

        self.f.place(x=posx, y=poxy)

    def clear(self):
        self.x1Entry.delete(0, END)
        self.y1Entry.delete(0, END)
        self.x2Entry.delete(0, END)
        self.x1Entry.focus_set()

    def getXY(self):
        return self.x1Entry.get(), self.y1Entry.get(), self.x2Entry.get()


class Xs_Ys_Form:
    def __init__(self, root, color, text, widthEntry=Settings.WIDTH_INPUT, command=None, btnText="btn", padx=5, pady=10, width=10,
                 font=('Arial', 11, 'bold'), fg="black", showButton=True, fields=["Start: ", "End: ", "Step: "]):
        self.showButton = showButton

        self.f = LabelFrame(root, bg=color, text=text, padx=padx, pady=pady, width=width, font=font, fg=fg)

        self.size = len(fields)
        self.widthEntry = widthEntry
        self.fg = fg

        self.entryes = []
        self.createEntryes()

        self.btn = Button(self.f, text=btnText, command=command)

        self.bind(command)

        self.fields = fields

    def createEntryes(self):
        for i in range(self.size):
            self.entryes.append(Entry(self.f, width=self.widthEntry))

    def insertXY(self, params):
        for e, p in zip(self.entryes, params):
            e.delete(0, END)
            e.insert(0, str(p))

    def bind(self, command):
        self.btn.bind("<Enter>", self.onEnter)
        self.btn.bind("<Leave>", self.onLeave)


        # ToDO не работают бинды
        for i in range(self.size - 1):
            self.entryes[i].bind("<Return>", lambda event: self.entryes[i + 1].focus_set())
            self.entryes[i].bind("<Down>", lambda event: self.entryes[i + 1].focus_set())

        for i in range(1, self.size):
            self.entryes[i].bind("<Up>", lambda event: self.entryes[i - 1].focus_set())

        if self.showButton:
            self.entryes[-1].bind("<Return>", lambda event: command())

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def show(self, color, posx=10, posy=10):
        self.f.propagate(0)

        for i in range(self.size * 2):
            if i % 2 == 0:
                Label(self.f, text=self.fields[i // 2], bg=color, font=('Arial', 10, 'bold'), fg=self.fg).grid(row=i)
            else:
                Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg=self.fg).grid(row=i)

        j = 0
        for i, e in enumerate(self.entryes):
            e.grid(row=j, column=1, sticky=W)
            j += 2

        if self.showButton:
            Label(self.f, text=" ", bg=color, font=('Arial', 1, 'bold'), fg="#f1e4de").grid(row=self.size * 2)
            self.btn.grid(row=self.size * 2 + 1, column=1, sticky="es")

        self.f.place(x=posx, y=posy)

    def clear(self):
        for e in self.entryes:
            e.delete(0, END)
        self.entryes[0].focus_set()

    def getXY(self):
        ans = []
        for e in self.entryes:
            ans.append(e.get())
        return ans

    def width(self):
        return self.f.winfo_width()

    def height(self):
        return self.f.winfo_reqheight()

