from __future__ import annotations


class Tile(int):
    def __new__(cls, value: int) -> Tile:
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other: object) -> Tile:
        if isinstance(other, Tile) or isinstance(other, int):
            res = super(Tile, self).__add__(other)
            return self.__class__(res)
        raise NotImplementedError

    def __sub__(self, other: object) -> Tile:
        if isinstance(other, Tile) or isinstance(other, int):
            res = super(Tile, self).__sub__(other)
            return self.__class__(res)
        raise NotImplementedError
