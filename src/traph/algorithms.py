import math
import time
from collections import deque
from typing import List, Tuple, Dict
from .graph import Graph
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

def load(graph: Graph) -> Tuple[Dict[int, Line], Dict[str, Circle]]:
    vertex_circle = dict()
    edge_line = dict()
    
    for i, val in enumerate(graph.v):
        center = graph.positions[i]
        circle = Circle(center)
        circle.draw(VERTEX_UNEXPLORED)
        vertex_circle[val] = circle

    for i in range(len(graph.e)):
        v1, v2 = graph.e[i]
        start, end = shortest_points(vertex_circle[v1], vertex_circle[v2])
        line = Line(start, end)
        line.draw(EDGE_UNEXPLORED)
        edge_line[i] = line

    return (edge_line, vertex_circle)

def sleep():
    time.sleep(0.5)

def bfs(lines: Dict[int, Line], circles: Dict[str, Circle], graph: Graph): 
    if not graph.v:
        return
    visited = set()
    start = graph.v[0]
    q = deque([start])
    sleep()
    circles[start].draw(VERTEX_CURRENT)
    visited.add(start)
    while q:
        c = q.popleft()
        sleep()
        circles[c].draw(VERTEX_EXPLORED)
        for i in graph.v_e[c]:
            sleep()
            lines[i].draw(EDGE_EXPLORED)
        for vert in graph.n[c]:
            if vert not in visited:
                q.append(vert)
                sleep()
                circles[vert].draw(VERTEX_CURRENT)
                visited.add(vert)

