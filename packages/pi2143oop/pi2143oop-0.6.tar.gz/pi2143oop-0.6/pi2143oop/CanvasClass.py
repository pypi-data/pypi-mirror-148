from .ErrorClass import Error
from .Settings import check_input, to_print


class Canvas:
    def __init__(self, default_symbol: str = '-', size: int = 40):
        self.size = size
        self.default_symbol = default_symbol
        self.Board = [default_symbol] * size * size

    def check_values(self, *args):
        x = [0]
        y = [0]

        if len(args) == 0:
            try:
                x = self.x
                y = self.y
            except:
                raise Error('У фигуры нет собственных точек')
        else:
            x = list(args)[::2]
            y = list(args)[1::2]

            if len(x) != len(y):
                raise Error('У точки не хватает аргумента x или y')

            check_input(x, self.size)
            check_input(y, self.size)

        return x, y

    def draw_dot(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.default_symbol

        x, y = self.check_values(*args)

        for i in range(len(x)):
            self.Board[x[i] + y[i] * self.size] = symbol[0]

    def fill(self, symbol: str = ''):
        if symbol == '':
            symbol = self.default_symbol

        self.Board = [symbol[0]] * self.size * self.size

    def get_dot(self, x=0, y=0):
        return self.Board[x + y * self.size]

    def print(self):
        a = list(range(self.size))

        print('    ', end='')
        for i in a:
            print(' ' * (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(self.size):
            print(' ' * (2 - len(str(i))) + str(i) + '  ', '  '.join(self.Board[i * self.size: (i + 1) * self.size]))

    def print_c(self, symbol: str = ''):
        if symbol == '':
            symbol = self.default_symbol

        to_print(self.Board, symbol[0])
