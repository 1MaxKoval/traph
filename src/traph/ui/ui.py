from typing import Tuple
from blessed import Terminal

TERMINAL = Terminal()
BACKGROUND_C = TERMINAL.black

TILE = '█'

def render(points: Tuple[int, int], color):
    for point in points:
        print(TERMINAL.move_xy(*point) + color + TILE + TERMINAL.normal)