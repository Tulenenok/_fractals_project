from model.Pivot import *


class Camera(BaseObj):
    def __init__(self, center, screenDist, field):
        super(Camera, self).__init__()

        self.pivot = Pivot(center)
        self.screenDist = screenDist   # Расстояние до проекционной плоскости
        self.field = field

    def move(self, vector):
        self.pivot.move(vector)

    def rotate(self, angle, axis):
        self.pivot.rotate(angle, axis)

    def observeRange(self):
        centerPoint = self.pivot.center
        leftPoint = Vector_3d(0, centerPoint.y, self.screenDist)
        rightPoint = Vector_3d(self.field.XEnd - self.field.XStart, centerPoint.y, self.screenDist)

        v1 = leftPoint - centerPoint
        v2 = rightPoint - centerPoint

        scale_prod = v1.scalar_product(v2)
        abs_v1 = abs(v1)
        abs_v2 = abs(v2)

        return math.acos(scale_prod / abs_v1 / abs_v2)

    # Вернет (x, y) для декартовых координат, которые нужно будет перевести
    # в координаты канвы известными методами
    def ScreenProection(self, vector: Vector_3d) -> Vector_2d:
        local = self.pivot.toLocalCoords(vector)

        # игнорируем точки сзади камеры

        if local.z < self.screenDist:
            return Vector_2d(None, None)

        angle = self.observeRange()
        width = self.field.XEnd - self.field.XStart
        scale = width / (2 * self.screenDist * math.tan(angle / 2))

        delta = self.screenDist / local.z
        prt = Vector_2d(local.x, local.y) * delta

        # Возвращаем точку только если она принадлежит экранной области
        if self.field.XStart <= prt.x < self.field.XEnd and self.field.YStart <= prt.y < self.field.YEnd:
            return prt

        return Vector_2d(None, None)