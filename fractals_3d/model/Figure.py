from model.Primitive import *


class Figure(Primitive):
    def __init__(self, color='blue', colorP='magenta', tag='pr'):
        super(Figure, self).__init__(color, colorP, tag)

    def fillVert(self, array):
        self.globalVertices.clear()
        self.localVertices.clear()

        for v in array:
            newV = Vector_3d(v[0], v[1], v[2])
            self.localVertices.append(newV)
            self.globalVertices.append(newV)

    def fillPol(self, array):
        self.polygons = array

    def fillCenter(self, x, y, z):
        self.pivot = Pivot((x, y, z))

    def loadFromTxt(self, filename):
        try:
            with open(filename, 'r') as f:
                n = int(f.readline())
                vers = []
                xSum, ySum, zSum = 0, 0, 0
                for i in range(n):
                    s = list(map(float, f.readline().split()))
                    xSum += s[0]
                    ySum += s[1]
                    zSum += s[2]
                    vers.append(s)
                xSum /= n
                ySum /= n
                zSum /= n
                f.readline()
                n = int(f.readline())
                pols = []
                for i in range(n):
                    s = list(map(int, f.readline().split()))
                    pols += s
        except:
            print('ERROR WITH READ')

        try:
            self.fillPol(pols)
            self.fillVert(vers)
            self.fillCenter(xSum, ySum, zSum)
        except:
            print('ERROR WITH FILL')