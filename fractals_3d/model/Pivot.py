from model.Vector import *


class Pivot(BaseObj):
    def __init__(self, center=(0, 0, 0), color='magenta', tag='pivot'):
        super(Pivot, self).__init__()

        self.center = Vector_3d(*center)

        x, y, z = center[0], center[1], center[2]
        self.X_axis = Vector_3d(1, 0, 0)
        self.Y_axis = Vector_3d(0, 1, 0)
        self.Z_axis = Vector_3d(0, 0, 1)

        self.color = color
        self.tag = tag

    def toLocalCoords(self, vector):
        localMatrix = Matrix([
            [self.X_axis.x, self.Y_axis.x, self.Z_axis.x],
            [self.X_axis.y, self.Y_axis.y, self.Z_axis.y],
            [self.X_axis.z, self.Y_axis.z, self.Z_axis.z]
        ])

        return localMatrix * (vector - self.center)

    def toGlobalCoords(self, vector):
        globalMatrix = Matrix([
            [self.X_axis.x, self.X_axis.y, self.X_axis.z],
            [self.Y_axis.x, self.Y_axis.y, self.Y_axis.z],
            [self.Z_axis.x, self.Z_axis.y, self.Z_axis.z]
        ])

        return (globalMatrix * vector) + self.center

    def move(self, vector):
        self.center += vector

    def rotate(self, angle, axis):
        self.X_axis = self.X_axis.rotate(angle, axis)
        self.Y_axis = self.Y_axis.rotate(angle, axis)
        self.Z_axis = self.Z_axis.rotate(angle, axis)

    def show(self, field, camera=None):
        center = Point_2d(self.center.x, self.center.y, color=self.color, tag=self.tag)
        center.show(field)

    def hide(self, field, **params):
        field.delete(self.tag)

    def reShow(self, field, camera=None):
        self.hide(field)
        field.update()
        self.show(field, camera)