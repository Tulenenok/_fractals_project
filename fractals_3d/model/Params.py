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

        self.rules = dict()
        self.__parseRules(rules)
        print(self.rules)

        self.n = int(float(n))
        self.color, self.width = color, int(float(width))

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
                                    [0, np.sin(angle), np.cos(angle)]], dtype='float64')

        self.HLU = tmp_matrix * self.HLU

    def getAll(self):
        return self.x, self.y, self.z, self.alpha, self.delta, self.step, self.axiom, self.rules, self.n, self.color, self.width

    def getCopy(self):
        return Params(*self.getAll())

    def __parseRules(self, stroke):
        def parseBeforeAfter(s):
            befInd = s.find('<')
            aftInd = s.find('<')

            before, after = "", ""

            if befInd != -1:
                before = s[:befInd]
                parent = s[befInd + 1:]

            if aftInd:
                after = s[aftInd + 1:]
                s = s[:aftInd]
            return before, s, after

        def parseParams(s):
            openInd = s.find('(')
            if openInd == -1:
                return s, tuple(), 'True'

            closeInd = s.find(')')
            params = list()
            letter = s[:openInd]

            for i in range(openInd + 1, closeInd):
                if s[i].isalpha():
                    params.append(s[i])

            condition = s[closeInd + 1:].strip()
            return letter, tuple(params), condition if condition != '' else 'True'

        if str(stroke).strip().startswith('{'):
            self.rules = eval(str(stroke))
            return

        lst = eval(str(stroke))
        for rule in lst:
            rule.strip()
            parent, child = rule.split(':')

            letter, params, condition = parseParams(parent)
            letter = letter.strip()
            if letter not in self.rules:
                self.rules[letter] = dict()

            if len(params) not in self.rules[letter]:
                self.rules[letter][len(params)] = dict()

            self.rules[letter][len(params)] = [params, condition, child.strip()]

            # if params not in self.rules[letter][len(params)]:
            #     self.rules[letter][len(params)][params] = dict()
            #
            # if condition not in self.rules[letter][len(params)][params]:
            #     self.rules[letter][len(params)][params][condition] = child.strip()


class Params2:
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

        self.n = int(float(n))
        self.color, self.width = color, int(float(width))

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
                                    [0, np.sin(angle), np.cos(angle)]], dtype='float64')

        self.HLU = tmp_matrix * self.HLU

    def getAll(self):
        return self.x, self.y, self.z, self.alpha, self.delta, self.step, self.axiom, self.rules, self.n, self.color, self.width

    def getCopy(self):
        return Params(*self.getAll())

    def __parseRules(self, stroke):
        def parseBeforeAfter(s):
            befInd = s.find('<')
            aftInd = s.find('<')

            before, after = "", ""

            if befInd != -1:
                before = s[:befInd]
                parent = s[befInd + 1:]

            if aftInd:
                after = s[aftInd + 1:]
                s = s[:aftInd]
            return before, s, after

        def parseParams(s):
            openInd = s.find('(')
            if openInd == -1:
                return s, tuple(), 'True'

            closeInd = s.find(')')
            params = list()
            letter = s[:openInd]

            for i in range(openInd + 1, closeInd):
                if s[i].isalpha():
                    params.append(s[i])

            condition = s[closeInd + 1:].strip()
            return letter, tuple(params), condition if condition != '' else 'True'

        self.rules = dict()

        for rule in stroke:
            rule.strip()
            parent, child = rule.split(':')

            letter, params, condition = parseParams(parent)
            if letter not in self.rules:
                self.rules[letter] = dict()

            if params not in self.rules[letter]:
                self.rules[letter][params] = dict()

            if condition not in self.rules[letter][params]:
                self.rules[letter][params][condition] = child.strip()

