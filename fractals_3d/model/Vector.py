from model.Point import *
import math


class Vector_2d(Point_2d):
    def __init__(self, x, y, **params):
        super(Vector_2d, self).__init__(x, y, **params)

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"

    def __eq__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector_2d):
            # Если other имеет тип Vector
            eps = 1e-6
            return math.fabs(self.x - other.x) < eps \
             and math.fabs(self.y - other.y) < eps
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __gt__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector_2d):
            # Если other имеет тип Vector
            return self.x > other.x and self.y > other.y
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __lt__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector_2d):
            # Если other имеет тип Vector
            return self.x < other.x and self.y < other.y
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector_2d(self.x * other, self.y * other)

        elif isinstance(other, float):
            return Vector_2d(self.x * other, self.y * other)

        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector_2d):
            return Vector_2d(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector_2d):
            return Vector_2d(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented


class Vector_3d(Point_3d):
    def __init__(self, x, y, z=0, **params):
        super(Vector_3d, self).__init__(x, y, z, **params)

    def __str__(self):
        return f"({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"

    def __eq__(self, other):
        eps = 1e-6
        return math.fabs(self.x - other.x) < eps and math.fabs(self.y - other.y) < eps and math.fabs(self.z - other.z)

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __mul__(self, other):
        return Vector_3d(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vector_3d(self.x / other, self.y / other, self.z / other)

    def __add__(self, other):
        return Vector_3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector_3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return f"Vector{str(self)}"

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def get_normal(self):
        x = self.x
        y = self.y

        return Vector_3d(y, -x, self.z)

    def get_orthogonal(self):
        length = abs(self)

        return Vector_3d(self.x / length, self.y / length, self.z / length)

    def get_orthogonal_normal(self):
        normal = self.get_normal()

        return normal.get_orthogonal()

    def rotate(self, angle, axis='x', **params):
        if axis == 'x':
            matrix = Matrix([[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]])
            return matrix * self

        if axis == 'y':
            matrix = Matrix([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
            return matrix * self

        if axis == 'z':
            matrix = Matrix([[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])
            return matrix * self


class Matrix:
    def __init__(self, fillArray):
        self.r = len(fillArray)
        self.c = len(fillArray[0])
        self.data = fillArray

    def __str__(self):
        ans = ''
        for i in range(self.r):
            for j in range(self.c):
                ans += str(self.data[i][j]) + ' '
            ans += '\n'
        return ans

    def __eq__(self, other):
        eps = 1e-6
        for i in range(self.r):
            for j in range(self.c):
                if math.fabs(self.data[i][j] - other.data[i][j]) > eps:
                    return False
        return True

    def __add__(self, other):
        for i in range(self.r):
            for j in range(self.c):
                self.data[i][j] += other.data[i][j]

    def __sub__(self, other):
        for i in range(self.r):
            for j in range(self.c):
                self.data[i][j] -= other.data[i][j]

    def __mul__(self, other):
        if isinstance(other, Vector_3d):
            ans = []
            for i in range(self.r):
                row = Vector_3d(*self.data[i])
                ans.append(row.scalar_product(other))
            return Vector_3d(*ans)

        if isinstance(other, Matrix):
            print('НЕ НАПИСАЛА')
