from typing import Tuple, List
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

    def __init__(self, point_generator, *args, **kwargs):
        self.points = list(set(point_generator(*args, **kwargs)))
        self.point_layers = {}
    
    def draw(self, /, color_map = None, text = None, text_f = None, text_b = None, fill = BACKGROUND_C):
        color_map = color_map if color_map is not None else {}        
        text = text if text is not None else {}
        text_f = text_f if text_f is not None else {}
        text_b = text_b if text_b is not None else {}
        for point in self.points:
            if point in color_map and point in text:
                # Handle the condition of a point being contained in text and in color tiles at the same time
                del color_map[point]
            if point not in color_map and point not in text:
                color_map[point] = fill
        self.point_layers = render(
            points=color_map,
            text_points=text,
            text_color=text_f,
            text_background=text_b
        )
    
    def erase(self):
        remove(self.points, self.point_layers)

class Circle(Shape):

    def __init__(self, center: Tuple[int, int], radius: int = CIRCLE_RADIUS):
        # Assuming valid center and radius
        super().__init__(circle_points, *center, radius)
        self.c = center
        self.r = radius

class Line(Shape):

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        super().__init__(bresenham, *start, *end)
        self.s = start
        self.e = end

class MessageBox(Shape):

    def __init__(self, position: str, message: str):
        if len(message) == 0:
            raise Exception('Message cannot be an empty string!')
        self.m = message
        max_width = 0
        height = 1
        line_width = 0
        for char in self.m:
            if char == '\n':
                height += 1
                line_width = 0
            else:
                line_width += 1
            max_width = max(max_width, line_width)

        self.height, self.width = height, max_width
        if position != 'c' and position != 'tl' and position != 'tr':
            raise Exception(f'Uknown position \'{position}\' for MessageBox')
        elif position == 'tl':
            top_left = (TERMINAL.width // 25, TERMINAL.height // 15)
        elif position == 'tr':
            offset_x, offset_y = TERMINAL.width // 25, TERMINAL.height // 15
            top_left = (TERMINAL.width - offset_x - self.width, offset_y)
        elif position == 'c':
            top_left = (TERMINAL.width // 2 - self.width // 2, TERMINAL.height // 2 - self.height // 2)

        self.top_left = top_left
        self.text_map = {}
        dx, dy = 0, 0
        ox, oy = top_left[0] + 1, top_left[1] + 1
        for char in self.m:
            if char == '\n':
                dy += 1
                dx = 0
                continue
            if dx > self.width:
                dx = 0
                dy += 1
            self.text_map[(ox + dx, oy + dy)] = char
            dx += 1
        super().__init__(rectangle_points, top_left, self.width + 2, self.height + 2)
    
    def draw(self, fill=TERMINAL.white, t_b='black', t_f='white'):
        text_background = {point: t_b for point in self.text_map}
        text_foreground = {point: t_f for point in self.text_map}
        super().draw(
            fill=fill, 
            text=self.text_map, 
            text_f=text_foreground,
            text_b=text_background
        )

class Bar(Shape):
    pass
