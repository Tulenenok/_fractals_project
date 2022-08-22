class BaseObj:
    ID = 0

    def __init__(self, **params):
        self.ID = BaseObj.ID
        BaseObj.ID += 1

        self._dictParams = params

    def __str__(self):
        return f'{type(self)} with ID = {self.ID}'

    def show(self, field, **params):
        pass

    def hide(self, field, **params):
        pass

    def reShow(self, field, **params):
        self.hide(field, **params)
        self.show(field, **params)

    def updateShowFlag(self, newFlag, **params):
        pass

    def rotate(self, **params):
        pass

    def scale(self, **params):
        pass

    def shift(self, **params):
        pass

    def move(self, **params):
        self.shift(**params)