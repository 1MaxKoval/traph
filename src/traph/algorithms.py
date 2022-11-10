import math
import time
from collections import deque
from typing import List, Tuple, Dict
from .ui.shapes import Circle, Line
from .ui.ui import TERMINAL

VERTEX_CHOOSING = TERMINAL.magenta3 
VERTEX_UNEXPLORED = TERMINAL.firebrick1
VERTEX_EXPLORED = TERMINAL.green
VERTEX_CURRENT = TERMINAL.aqua

EDGE_CHOOSING = TERMINAL.magenta3
EDGE_UNEXPLORED = TERMINAL.firebrick1
EDGE_EXPLORED = TERMINAL.green
EDGE_CURRENT = TERMINAL.aqua

def distance_formula(x0: int, y0: int, x1: int, y1: int) -> float:
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

def shortest_points(circle0: Circle, circle1: Circle) -> List[Tuple]:
    p0, p1 = circle0.points, circle1.points
    if not p0 or not p1:
        return [(-1,-1), (-1,-1)]
    shortest = float('inf')
    for p0_point in p0:
        for p1_point in p1:
            c = distance_formula(*p0_point, *p1_point)
            if c < shortest:
                result = [p0_point, p1_point]
                shortest = c
    return result

def sleep():
    time.sleep(0.5)

def bfs(start: str, lines: Dict[Tuple[str, str], Line], circles: Dict[str, Circle], neighbors: Dict[str, List[str]]): 
    if not circles:
        return
    visited = set()
    q = deque([start])
    sleep()
    circles[start].erase()
    circles[start].draw(fill=VERTEX_CURRENT)
    visited.add(start)
    while q:
        c = q.popleft()
        sleep()
        circles[c].erase()
        circles[c].draw(fill=VERTEX_EXPLORED)
        for neighbor in neighbors[c]:
            sleep()
            line = lines[(c, neighbor)]
            line.erase()
            line.draw(fill=EDGE_EXPLORED)
        for vert in neighbors[c]:
            if vert not in visited:
                q.append(vert)
                sleep()
                circles[vert].erase()
                circles[vert].draw(fill=VERTEX_CURRENT)
                visited.add(vert)