from typing import Tuple
from blessed import Terminal

TERMINAL = Terminal()
BACKGROUND_C = TERMINAL.black

TILE = '█'

# Used for keeping track of color layers
layers = []

def render(points: Tuple[int, int], color):
    for point in points:
        record_on_layer(*point, color)
        print(TERMINAL.move_xy(*point) + color + TILE + TERMINAL.normal)

def remove(points: Tuple[int, int]):
    for point in points:
        found = False
        for i in range(len(layers) - 1, -1, -1):
            if point in layers[i]:
                found = True
                del layers[i][point]
                if i - 1 != -1:
                    print(TERMINAL.move_xy(*point) + layers[i-1][point] + TILE + TERMINAL.normal)
                else:
                    print(TERMINAL.move_xy(*point) + BACKGROUND_C + TILE + TERMINAL.normal)
                break
        if not found:
            print(TERMINAL.move_xy(*point) + BACKGROUND_C + TILE + TERMINAL.normal)

def record_on_layer(x: int, y: int, color):
    for i in range(len(layers) - 1, -1, -1):
        if (x, y) in layers[i]:
            if i + 1 == len(layers):
                layers.append({(x, y): color})
            else:
                layers[i + 1][(x, y)] = color
            return
    layers.append({(x, y): color})
