from .ErrorClass import Error
from .Settings import check_input, to_print


class Dot():
    def __init__(self, canvas, x: int = 0, y: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self.check_values(x, y)

    def check_values(self, *args):
        x = [0]
        y = [0]

        if len(args) == 0:
            try:
                x = self.x
                y = self.y
            except:
                raise Error('У фигуры нет собственных точек. Укажите входные данные')
        else:
            x = list(args)[::2]
            y = list(args)[1::2]

            if len(x) != len(y):
                raise Error('У точки не хватает аргумента x или y')

            check_input(x, self.cnv.size)
            check_input(y, self.cnv.size)

        return x, y

    def set_dots(self, x: list, y: list):
        dots = []
        for i in range(len(x)):
            dots.append(x[i])
            dots.append(y[i])

        return dots

    def set_fill_dots(self, x: list, y: list):
        dots = self.set_dots(x, y)
        x = []
        y = []
        for i in range(0, len(dots), 2):
            x.append(dots[i])
            y.append(dots[i + 1])

        dots = []

        for i in range(len(y)):
            for j in range(len(y)):
                if y[i] == y[j]:
                    for k in range(min(x[i], x[j]) + 1, max(x[i], x[j])):
                        dots.append(k)
                        dots.append(y[i])

        return dots

    def draw(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self.check_values(*args)

        dots = self.set_dots(x, y)

        for i in range(1, len(dots), 2):
            self.Board[dots[i - 1] + dots[i] * self.cnv.size] = symbol[0]

    def draw_dot(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self.check_values(*args)

        for i in range(len(x)):
            self.Board[x[i] + y[i] * self.cnv.size] = symbol[0]

    def fill(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self.check_values(*args)

        symbol2 = self.get_dot(x[0], y[0])

        dots = self.set_fill_dots(x, y)
        self.draw_dot(symbol[0], *dots)

        dots = self.set_dots(x, y)
        self.draw_dot(symbol2, *dots)

    def get_dot(self, x=0, y=0):
        return self.Board[x + y * self.cnv.size]

    def draw_c(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self.check_values(*args)

        dots = self.set_dots(x, y)
        for i in range(len(x)):
            dots.append(x[i])
            dots.append(y[i])

        self.cnv.draw_dot(symbol, *dots)

    def print(self):
        a = list(range(self.cnv.size))

        print('    ', end='')
        for i in a:
            print(' ' * (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(self.cnv.size):
            print(' ' * (2 - len(str(i))) + str(i) + '  ',
                  '  '.join(self.Board[i * self.cnv.size: (i + 1) * self.cnv.size]))

    def print_c(self, symbol: str = ''):
        if symbol == '':
            symbol = self.cnv.default_symbol

        to_print(self.Board, symbol[0])

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
        return 0
