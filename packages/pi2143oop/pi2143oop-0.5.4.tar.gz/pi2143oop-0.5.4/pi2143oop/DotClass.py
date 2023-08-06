from .ErrorClass import Error
from .MainClass import canvas


def check_input(x: list, size: int):
    s = 'На вход подаются числа от (0) до (размер поля - 1)'

    for i in x:
        if not isinstance(i, int):
            raise Error(s)
        elif i >= size or i < 0:
            raise Error(s)


class Dot():
    def __init__(self, x: int = 0, y: int = 0):
        self.size = canvas.size
        self.default_symbol = canvas.default_symbol
        self.Board = [self.default_symbol] * self.size * self.size

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

            check_input(x, self.size)
            check_input(y, self.size)

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
            symbol = self.default_symbol

        x, y = self.check_values(*args)

        dots = self.set_dots(x, y)

        for i in range(1, len(dots), 2):
            self.Board[dots[i - 1] + dots[i] * self.size] = symbol[0]

    def draw_dot(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.default_symbol

        x, y = self.check_values(*args)

        for i in range(len(x)):
            self.Board[x[i] + y[i] * self.size] = symbol[0]

    def fill(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.default_symbol

        x, y = self.check_values(*args)

        symbol2 = self.get_dot(x[0], y[0])

        dots = self.set_fill_dots(x, y)
        self.draw_dot(symbol[0], *dots)

        dots = self.set_dots(x, y)
        self.draw_dot(symbol2, *dots)

    def get_dot(self, x=0, y=0):
        return self.Board[x + y * self.size]

    def draw_c(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.default_symbol

        x, y = self.check_values(*args)

        dots = self.set_dots(x, y)
        for i in range(len(x)):
            dots.append(x[i])
            dots.append(y[i])

        canvas.draw_dot(symbol, *dots)

    def print(self):
        a = list(range(self.size))

        print('    ', end='')
        for i in a:
            print(' ' * (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(self.size):
            print(' ' * (2 - len(str(i))) + str(i) + '  ', '  '.join(self.Board[i * self.size: (i + 1) * self.size]))

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