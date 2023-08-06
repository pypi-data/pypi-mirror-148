from math import pi

from .ErrorClass import Error
from .LineClass import Line
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


class Rectangle(Dot):
    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self.check_values(x1, y1, x2, y2)

    def set_dots(self, x: list, y: list):
        dots = []

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            dots.append(i)
            dots.append(y[0])
            dots.append(i)
            dots.append(y[1])
        for i in range(min(y[0], y[1]) + 1, max(y[0], y[1])):
            dots.append(x[0])
            dots.append(i)
            dots.append(x[1])
            dots.append(i)

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
        s = abs(self.__x[0] - self.__y[1]) * abs(self.__x[1] - self.__y[0])

        return s


class Triangle(Dot):
    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, x3: int = 0, y3: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self.check_values(x1, y1, x2, y2, x3, y3)

        self.a = ((self.__x[0] - self.__x[1]) ** 2 + (self.__y[0] - self.__y[1]) ** 2) ** 0.5
        self.b = ((self.__x[0] - self.__x[2]) ** 2 + (self.__y[0] - self.__y[2]) ** 2) ** 0.5
        self.c = ((self.__x[1] - self.__x[2]) ** 2 + (self.__y[1] - self.__y[2]) ** 2) ** 0.5

        self.check_triangle()

    def check_triangle(self):
        if not (self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a):
            raise Error('Невозможно построить такой треугольник')

    def set_dots(self, x: list, y: list):
        dots = []

        l1 = Line(self.cnv, x[0], y[0], x[1], y[1])
        l2 = Line(self.cnv, x[0], y[0], x[2], y[2])
        l3 = Line(self.cnv, x[1], y[1], x[2], y[2])
        l = [l1, l2, l3]

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
        p = (self.a + self.b + self.c) / 2

        s = (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

        return s


class Square(Rectangle):
    def __init__(self, canvas, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y = self.check_values(x1, y1, x2, y2)
        self.set_square()

    def set_square(self):
        if abs(self.__x[0] - self.__x[1]) != abs(self.__y[0] - self.__y[1]):
            if self.__y[0] < self.__y[1]:
                self.__y[1] = self.__y[0] + abs(self.__x[0] - self.__x[1])
            else:
                self.__y[0] = self.__y[1] + abs(self.__x[0] - self.__x[1])

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
        s = abs(self.__x[0] - self.__y[1]) ** 2

        return s


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


class Circle(Dot):
    def __init__(self, canvas, x: int = 0, y: int = 0, r: int = 0):
        self.cnv = canvas
        self.Board = [self.cnv.default_symbol] * self.cnv.size * self.cnv.size

        self.__x, self.__y, self.__r = self.check_circle(x, y, r)

    def check_circle(self, *args):
        x, y, r = args

        check_input([x], self.cnv.size)
        check_input([y], self.cnv.size)
        check_input([r], self.cnv.size)

        if x + r >= self.cnv.size or x + r < 0 or y + r >= self.cnv.size or y - r < 0:
            raise Error('Фигура выходит за пределы поля')

        if r == 0:
            raise Error('Радиус должен быть больше 0')

        return [x], [y], r

    def get_value_y(self, x: int):
        return (self.__r ** 2 - (x - self.__x[0]) ** 2) ** 0.5

    def get_value_x(self, y: int):
        return (self.__r ** 2 - (y - self.__y[0]) ** 2) ** 0.5

    def set_line_y(self, x: list):
        dots = []

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = self.get_value_y(i) + self.__y[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(i)
                        dots.append(int(k))
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k + 1))
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k))

        for i in range(min(x[0], x[1]), max(x[0], x[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = -self.get_value_y(i) + self.__y[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(i)
                        dots.append(int(k))
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k + 1))
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(i)
                                dots.append(int(k))

        return dots

    def set_line_x(self, y: list):
        dots = []

        for i in range(min(y[0], y[1]), max(y[0], y[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = self.get_value_x(i) + self.__x[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(int(k))
                        dots.append(i)
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(int(k + 1))
                                dots.append(i)
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(int(k))
                                dots.append(i)

        for i in range(min(y[0], y[1]), max(y[0], y[1]) + 1):
            if 0 <= i <= self.cnv.size:
                k = -self.get_value_x(i) + self.__x[0]

                if 0 <= int(k) <= self.cnv.size:
                    if int(k) == float(k):
                        dots.append(int(k))
                        dots.append(i)
                    else:
                        a = k - int(k)

                        if a >= 0.4:
                            if 0 <= int(k + 1) <= self.cnv.size:
                                dots.append(int(k + 1))
                                dots.append(i)
                        if a <= 0.6:
                            if 0 <= int(k) <= self.cnv.size:
                                dots.append(int(k))
                                dots.append(i)

        return dots

    def set_dots(self, x: list, y: list):
        dots = []

        x = [x[0] - self.__r, x[0] + self.__r]
        dots.extend(self.set_line_y(x))
        y = [y[0] - self.__r, y[0] + self.__r]
        dots.extend(self.set_line_x(y))

        return dots

    def fill(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        x, y = self.check_values(*args)

        symbol2 = self.get_dot(x[0] - self.__r, y[0])

        dots = self.set_fill_dots(x, y)
        self.draw_dot(symbol[0], *dots)

        dots = self.set_dots(x, y)
        self.draw_dot(symbol2, *dots)

    def cut_piece(self, symbol: str = '', x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        if symbol == '':
            symbol = self.cnv.default_symbol

        t = Triangle(x1, y1, x2, y2, self.__x[0], self.__y[0])

        dots = t.set_dots(t.x, t.y)
        dots.extend(t.set_fill_dots(t.x, t.y))

        self.draw_dot(symbol[0], *dots)

    def draw_c(self, symbol: str = '', *args):
        if symbol == '':
            symbol = self.cnv.default_symbol

        dots = []
        for y in range(self.cnv.size):
            k = self.Board[y * self.cnv.size: (y + 1) * self.cnv.size]
            if symbol[0] in k:
                for x in range(len(k)):
                    if k[x] == symbol[0]:
                        dots.append(x)
                        dots.append(y)

        self.cnv.canvas.draw_dot(symbol, *dots)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def r(self):
        return self.__r

    @property
    def xyr(self):
        return True

    @xyr.setter
    def xyr(self, *args):
        self.__x, self.__y, self.__r = self.check_circle(*args[0])

    @property
    def square(self):
        s = pi * self.__r ** 2
