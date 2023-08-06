from .ErrorClass import Error
from .CanvasClass import Canvas
from .DotClass import Dot

canvas = None


class Main():
    def __init__(self, symbol: str = '-', size: int = 40):
        canvas = Canvas(symbol[0], size)
        self.default_font_color = 37
        self.default_background_color = 40
        self.font_color = 31
        self.background_color = 40
