from tkinter import *
from tkinter.messagebox import *
from model.Tools import Tools
from view.Settings import Settings
# from view.Btn import WrapButton
from view.Point_2d import Point_2d


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

