from .ErrorClass import Error
from .CanvasClass import Canvas
from .DotClass import Dot


class Main():
    canvas = None

    def __init__(self, symbol: str = '-', size: int = 40):
        self.canvas = Canvas(symbol[0], size)
        self.default_font_color = 37
        self.default_background_color = 40
        self.font_color = 31
        self.background_color = 40

    def to_print(self, board: list, symbol: str):
        size = int(len(board) ** 0.5)

        a = list(range(size))

        print('\033[{1}m\033[{0}m    '.format(self.default_font_color, self.default_background_color), end='')
        for i in a:
            print('\033[{1}m\033[{0}m '.format(self.default_font_color, self.default_background_color) *
                  (2 - len(str(i))) + str(i), end=' ')
        print('\n')

        for i in range(size):
            print('\033[{0}m\033[{1}m '.format(self.default_font_color, self.default_background_color) *
                  (2 - len(str(i))) + str(i), end='   ')

            k = board[i * size: (i + 1) * size]

            for j in k:
                if j == symbol[0]:
                    print('\033[{1}m\033[{0}m{2}  '.format(self.default_font_color, self.default_background_color, j),
                          end='')
                else:
                    print('\033[{1}m\033[{0}m{2}  '.format(self.font_color, self.background_color, j), end='')

            print()


    def check_input(x: list, size: int):
        s = 'На вход подаются числа от (0) до (размер поля - 1)'

        for i in x:
            if not isinstance(i, int):
                raise Error(s)
            elif i >= size or i < 0:
                raise Error(s)
