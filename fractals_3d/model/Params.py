import math

from controll.Tools import *
import numpy as np


class Params:
    def __init__(self, startX, startY, startZ,
                 startAlpha,
                 delta, d,
                 axiom, rules,
                 n, color='blue', width=2):

        self.x, self.y, self.z = startX, startY, startZ
        self.alpha, self.delta = startAlpha, delta
        self.step = float(d)

        self.axiom = axiom
        self.rules = rules if type(rules) == dict else eval('{' + str(rules) + '}')

        self.n = int(n)
        self.color, self.width = color, int(width)

        self.HLU = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float64')
        self.rotate(math.radians(self.alpha), 'U')

    def __str__(self):
        return f'(x, y, z) = {self.x, self.y, self.z}\n' \
               f'alpha = {self.alpha}\n' \
               f'axiom = {self.axiom}\n' \
               f'rules = {self.rules}\n'

    def __getattribute__(self, item):
        if item == 'x' or item == 'y' or item == 'z' or item == 'alpha' or item == 'delta':
            tmp = object.__getattribute__(self, item)
            return float(tmp) if Tools.isFloat(tmp) else eval(tmp)
        else:
            return object.__getattribute__(self, item)


    def rotate(self, angle, axis='H'):
        # Вокруг Z
        if axis == 'U':
            tmp_matrix = np.matrix([[np.cos(angle), np.sin(angle), 0],
                                   [-np.sin(angle), np.cos(angle), 0],
                                   [0, 0, 1]], dtype='float64')

        # Вокруг Y
        if axis == 'L':
            tmp_matrix = np.matrix([[np.cos(angle), 0, -np.sin(angle)],
                                    [0, 1, 0],
                                    [np.sin(angle), 0, np.cos(angle)]], dtype='float64')

        # Вокруг Х
        if axis == 'H':
            tmp_matrix = np.matrix([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), 0, np.cos(angle)]], dtype='float64')

        self.HLU = tmp_matrix * self.HLU

    def getAll(self):
        return self.x, self.y, self.z, self.alpha, self.delta, self.step, self.axiom, self.rules, self.n, self.color, self.width

    def getCopy(self):
        return Params(*self.getAll())
