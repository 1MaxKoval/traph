from typing import Tuple, List, Dict, Callable
from blessed import Terminal

TERMINAL = Terminal()
BACKGROUND_C = TERMINAL.black

TILE = '█'

class TextPoint:

    def __init__(self, character, foreground_color, background_color):
        self.c = character
        self.f = foreground_color
        self.b = background_color

# Used for keeping track of colors assosciated with particular layers
layers = []

def blessed_colors(foreground_c: str, background_c: str) -> Callable:
    if foreground_c == 'red' and background_c == 'green':
        return TERMINAL.red_on_green
    else:
        return TERMINAL.black_on_white

def set_og_background():
    print(TERMINAL.home + TERMINAL.on_black + TERMINAL.clear)

def remove(points: List[Tuple[int, int]], point_layers: Dict[Tuple[int, int], int]):
    for point in points:
        point_layer = point_layers[point]
        # BUG: For some reason a point_layer is has been deleted for a shape before its .erase() has been called.
        del layers[point_layer][point]
        highest_layer = get_top_layer(*point)
        if highest_layer == -1:
            print(TERMINAL.move_xy(*point) + BACKGROUND_C + TILE + TERMINAL.normal)
        elif highest_layer < point_layer:
            data = layers[highest_layer][point]
            if isinstance(data, TextPoint):
                painter = blessed_colors(data.f, data.b)
                print(TERMINAL.move_xy(*point) + painter(data.c) + TERMINAL.normal)
            else:
                print(TERMINAL.move_xy(*point) + data + TILE + TERMINAL.normal)

def get_top_layer(x: int, y: int) -> int:
    point = (x, y)
    for i in range(len(layers) - 1, -1, -1):
        if point in layers[i]:
            return i
    return -1

def add_point_layer(point, data) -> int:
    for i in range(len(layers) - 1, -1, -1):
            if point in layers[i]:
                if i + 1 == len(layers):
                    layers.append({point: data})
                else:
                    layers[i + 1][point] = data
                return i + 1
    if not layers:
        layers.append({point: data})
    else:
        layers[0][point] = data
    return 0

def render(points: Dict[Tuple, str] = None,  text_points: Dict[Tuple, str] = None, text_color: Dict[Tuple, str] = None, text_background: Dict[Tuple, str] = None) -> Dict[Tuple, int]:
    # Assumes there is no overlap between text_points and points
    points = dict() if points is None else points
    text_color = dict() if text_color is None else text_color
    text_points = dict() if text_points is None else text_points
    text_background = dict() if text_background is None else text_background

    point_layers = dict()
    for point, color in points.items():
        layer = add_point_layer(point, color)
        point_layers[point] = layer
        print(TERMINAL.move_xy(*point) + color + TILE + TERMINAL.normal)

    for point, char in text_points.items():
        background_c = text_background[point] if point in text_background else BACKGROUND_C
        foreground_c = text_color[point] if point in text_color else BACKGROUND_C
        color_point = TextPoint(char, foreground_c, background_c)
        layer = add_point_layer(point, color_point)
        point_layers[point] = layer
        painter = blessed_colors(foreground_c, background_c)
        print(TERMINAL.move_xy(*point) + painter(char) + TERMINAL.normal)

    return point_layers
