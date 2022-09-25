from typing import Tuple, List, Callable
from .ui import render, remove, BACKGROUND_C, TERMINAL
from bresenham import bresenham

CIRCLE_RADIUS = 2

def reflect_octants(x: int, y: int, x_c: int, y_c:int) -> List[Tuple]:
    """
    Computes the coordinates in all octants of a circle
    """
    result = [
        (x + x_c, y + y_c),
        (-x + x_c, y + y_c),
        (x + x_c, -y + y_c),
        (-x + x_c, -y + y_c),
        (y + x_c, x + y_c),
        (-y + x_c, x + y_c),
        (y + x_c, -x + y_c),
        (-y + x_c, -x + y_c)
    ]
    return result

def rectangle_points(top_left: Tuple[int, int], hor: int, vert: int) -> List[Tuple[int, int]]:
    res = list()
    for dy in range(0, vert):
        for dx in range(0, hor):
            res.append( (top_left[0] + dx, top_left[1] + dy) )
    return res

def circle_points(x_o: int, y_o: int, r: int) -> List[Tuple[int, int]]:
    """
    Generates points for a circle
    
    https://www.geeksforgeeks.org/mid-point-circle-drawing-algorithm/
    """
    point_result = list()
    r = abs(r)
    if r == 0:
        point_result.append( (x_o, y_o) )
        return point_result

    e = 1 - r
    x, y = r, 0
    while x >= y:
        point_result.extend(reflect_octants(x, y, x_o, y_o))
        y += 1
        if e <= 0:
            e = e + 2*(y + 1) + 1
        else:
            x -= 1
            e = e + 2*(y + 1) - 2*(x - 1) + 1
    return point_result

class Shape:

    def __init__(self):
        self.points = []
        self.point_layers = []
    
    def draw(self, color):
        point_color_map = {point : color for point in self.points}
        self.point_layers = render(points = point_color_map)
    
    def erase(self):
        remove(self.points, self.point_layers)

class Circle(Shape):

    def __init__(self, center: Tuple[int, int], radius: int = CIRCLE_RADIUS):
        # Assuming valid center and radius
        super().__init__()
        self.c = center
        self.r = radius
        self.points = list(set(circle_points(*center, radius)))

class Line(Shape):

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        super().__init__()
        self.s = start
        self.e = end
        self.points = list(bresenham(*start, *end))

class MessageBox(Shape):

    def __init__(self, position: str, message: str):
        super().__init__()

        self.m = message
        max_width = 0
        height = 0
        line_width = 0
        for char in message:
            if char == '\n':
                height += 1
                max_width = max(max_width, line_width)
                line_width = 0 
            else:
                line_width += 1

        self.height, self.width = height, max_width
        if position != 'c' and position != 'tl' and position != 'tr':
            raise Exception()
        elif position == 'tl':
            top_left = (TERMINAL.width // 25, TERMINAL.height // 15)
        elif position == 'tr':
            offset_x, offset_y = TERMINAL.width // 25, TERMINAL.height // 15
            top_left = (TERMINAL.width - offset_x - self.width, offset_y)
        elif position == 'c':
            top_left = (TERMINAL.width // 2 - self.width // 2, TERMINAL.height // 2 - self.height // 2)

        # Add 2 to have a 1 pixel border on each side
        self.top_left = top_left
        self.points = rectangle_points(top_left, self.width + 2, self.height + 2)
    
    def draw(box_color, text_foreground = 'black', text_background = 'white'):
        pass

class Bar(Shape):
    pass
