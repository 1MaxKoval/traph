from typing import Tuple, List
from blessed import Terminal

TERMINAL = Terminal()
BACKGROUND_C = TERMINAL.black

TILE = '█'

# Used for keeping track of color layers
layers = []

def remove(points: Tuple[int, int], point_layers=None):
    if point_layers is None:
        point_layers = []

    for point, point_layer in zip(points, point_layers):
        del layers[point_layer][point]
        highest_layer = get_top_layer(point)
        if highest_layer == -1:
            print(TERMINAL.move_xy(*point) + BACKGROUND_C + TILE + TERMINAL.normal)
        elif highest_layer < point_layer:
            print(TERMINAL.move_xy(*point) + layers[highest_layer][point] + TILE + TERMINAL.normal)

def get_top_layer(x: int, y: int) -> int:
    point = (x, y)
    for i in range(len(layers) - 1, -1, -1):
        if point in layers[i]:
            return i
    return -1

def render(points, color) -> List[int]:
    point_layers = []
    for point in points:
        x, y = point
        added = False
        for i in range(len(layers) - 1, -1, -1):
            if (x, y) in layers[i]:
                added = True
                point_layers.append(i)
                if i + 1 == len(layers):
                    layers.append({(x, y): color})
                else:
                    layers[i + 1][(x, y)] = color
                break 
        # Case: Point does not exist in any of the layers
        if not added:
            if not layers:
                layers.append({(x, y): color})
            else:
                layers[0][(x, y)] = color
        print(TERMINAL.move_xy(x, y) + color + TILE + TERMINAL.normal)
    return point_layers
