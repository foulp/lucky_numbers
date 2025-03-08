class Tile(int):
    def __new__(cls, value: int):
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other):
        res = super(Tile, self).__add__(other)
        return self.__class__(res)

    def __sub__(self, other):
        res = super(Tile, self).__sub__(other)
        return self.__class__(res)
