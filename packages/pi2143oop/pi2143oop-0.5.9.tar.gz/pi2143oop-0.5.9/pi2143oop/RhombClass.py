from .ErrorClass import Error
from .DotClass import Dot
from .LineClass import Line
from .Settings import check_input


class Rhomb(Dot):
    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self.check_rhomb(x1, y1, x2, y2)

    def check_rhomb(self, *args):
        x = list(args)[::2]
        y = list(args)[1::2]

        if len(x) != len(y):
            raise Error('У точки не хватает аргумента x или y')

        check_input(x, self.cnv.size)
        check_input(y, self.cnv.size)

        if x[1] + x[1] - x[0] >= self.cnv.size or y[0] + y[0] - y[1] >= self.cnv.size:
            raise Error('Фигура выходит за пределы поля')

        return x, y

    def set_dots(self, x: list, y: list):
        dots = []

        d1 = Line(self.cnv, x[0], y[0], x[1] + x[1] - x[0], y[0])
        d2 = Line(self.cnv, x[1], y[1], x[1], y[0] + y[0] - y[1])
        l1 = Line(self.cnv, x[0], y[0], x[1], y[1])
        l2 = Line(self.cnv, x[0], y[0], x[1], y[0] + y[0] - y[1])
        l3 = Line(self.cnv, x[1] + x[1] - x[0], y[0], x[1], y[1])
        l4 = Line(self.cnv, x[1] + x[1] - x[0], y[0], x[1], y[0] + y[0] - y[1])
        l = [d1, d2, l1, l2, l3, l4]

        for i in l:
            dots.extend(i.set_dots())

        return dots

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def xy(self):
        return True

    @xy.setter
    def xy(self, *args):
        self.__x, self.__y = self.check_values(*args[0])

    @property
    def square(self):
        s = 2 * (self.__x[1] - self.__x[0]) * (self.__y[0] - self.__y[1])

        return s
