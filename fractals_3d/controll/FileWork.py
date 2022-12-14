import tkinter.filedialog as fd
from model.Figure import Figure
from controll.Settings import Settings
from controll.Tools import Tools
import canvasvg

import pandas as pd


class FileWork:

    NAMES = ['X', 'Y', 'Z', 'Alpha', 'Axiom', 'Rule', 'Step', 'Delta', 'N', 'Constants', 'Bg', 'Line', 'Width']

    @staticmethod
    def loadFigure():
        filetypes = (("Txt", '*.txt'), ("Excel", "*.xlsx"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir=Settings.DIR_INPUT_POINTS,
                                      filetypes=filetypes, multiple=False)
        if filename:
            newFigure = Figure()
            newFigure.loadFromTxt(filename)
            return newFigure

    @staticmethod
    def readData(filename):
        if not Tools.isRightFilename(filename) or filename[-5::] != '.xlsx':
            return Tools.INVALID_FILENAME

        try:
            xl = pd.ExcelFile(filename.replace('\\', '\\\\'))
            list_points = xl.parse(xl.sheet_names[0])
            data = list_points[FileWork.NAMES]
            newData = [list(data[i])[0] if i != 'Rule' and i != 'Constants' else list(data[i].dropna()) for i in FileWork.NAMES]
        except:
            print("Error with file")
            return []

        print(newData)

        return newData

    @staticmethod
    def loadData(startParams, fractalParams, colorsParams):
        filetypes = (("Excel", "*.xlsx"), ("Txt", '*.txt'))
        filename = fd.askopenfilename(title="Открыть файл", initialdir=Settings.DIR_INPUT_POINTS,
                                      filetypes=filetypes, multiple=False)
        if filename and filename[-5::] == '.xlsx':
            coords = FileWork.readData(filename)

            if not coords:
                print("aaa")
                return

            startParams.insertXY(coords[:4])
            fractalParams.insertXY((coords[4:10]))
            colorsParams.insertXY(coords[10:])

    @staticmethod
    def saveData(startParams, fractalParams, colorsParams):
        new_file = fd.asksaveasfile(title="Сохранить файл", defaultextension=".xlsx",
                                    filetypes=(("Excel", "*.xlsx"),))
        if new_file:
            d1 = startParams.getXY()
            d1 += fractalParams.getXY()
            d1 += colorsParams.getXY()
            d1 = list(map(str, d1))
            df = pd.DataFrame([d1], columns=FileWork.NAMES)

            with pd.ExcelWriter(new_file.name) as writer:
                df.to_excel(writer)
                print('OK save')

    @staticmethod
    def saveCanva(canva):
        new_file = fd.asksaveasfile(title="Сохранить канву", defaultextension=".svg",
                                    filetypes=(("svg", "*.svg"),))
        if new_file:
            canvasvg.saveall(new_file.name, canva)