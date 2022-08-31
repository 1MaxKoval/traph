from typing import Tuple, List
from .ui import render, BACKGROUND_C
from bresenham import bresenham

CIRCLE_RADIUS = 1

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

class Circle:

    def __init__(self, center: Tuple[int, int], radius: int = CIRCLE_RADIUS):
        # Assuming valid center and radius
        self.c = center
        self.r = radius
        self.points = set(circle_points(*center, radius))
    
    def draw(self, color):
        render(self.points, color)
    
    def erase(self):
        render(self.points, BACKGROUND_C)

class Line:

    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        # Assuming valid center and radius
        self.s = start
        self.e = end
        self.points = set(bresenham(*start, *end))
    
    def draw(self, color):
        render(self.points, color)
    
    def erase(self):
        render(self.points, BACKGROUND_C)