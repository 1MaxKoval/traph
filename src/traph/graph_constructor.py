from typing import List, Dict
from .graph import Graph
from .ui.ui import set_og_background, TERMINAL as term
from .ui.shapes import MessageBox, Circle, Line, CIRCLE_RADIUS
from .algorithms import shortest_points
from collections import defaultdict


def construct_graph() -> Graph:
    set_og_background()
    welcome_msg = \
"""Welcome to Traph!
A graph algorithm visualiser that runs in your terminal/cmd!
Press `1` to start graph construction."""
    welcome_box = MessageBox('c', welcome_msg)
    welcome_box.draw()
    with term.cbreak():
        val = ''
        while val != '1':
            val = term.inkey()
        welcome_box.erase()
    del welcome_box
    menu_msg = \
"""1. Add vertex
2. Remove vertex
3. Add edge
4. Remove edge
5. Select algorithm"""
    menu_box = MessageBox('c', menu_msg)
    menu_box.draw() 
    circles = []
    lines = []
    edges = defaultdict(list)
    while True:
        with term.cbreak():
            val = ''
            while val not in {'1', '2', '3', '4', '5'}:
                val = term.inkey()
                if val == '1':
                    menu_box.erase()
                    circles.append(add_vertex())
                    menu_box.draw()
                elif val == '2':
                    menu_box.erase()
                elif val == '3' and len(circles) >= 2:
                    menu_box.erase()
                    lines.append(add_edge(circles, edges))
                    menu_box.draw()
                elif val == '4':
                    menu_box.erase()
                elif val == '5':
                    menu_box.erase()

def add_vertex() -> Circle:
    # ENTER -> 343
    # LEFT -> 260
    # RIGHT -> 261
    # UP -> 259
    # DOWN -> 258 
    pos = (term.width // 2, term.height // 2)
    c = Circle(pos)
    c.draw(fill=term.green)
    top_msg = """Position the vertex and press `ENTER`"""
    helper_msg_box = MessageBox('tl', top_msg) 
    helper_msg_box.draw()
    val = term.inkey()
    while not val.is_sequence or val.code != 343:
        if val.is_sequence:
            if val.code == 260:
                c.erase()
                if (pos[0] - 1 - CIRCLE_RADIUS) >= 0: 
                    pos = (pos[0] - 1, pos[1])
                c = Circle(pos)
                c.draw(fill=term.green)
            elif val.code == 261:
                c.erase()
                if (pos[0] + 1 + CIRCLE_RADIUS) <= term.width: 
                    pos = (pos[0] + 1, pos[1])
                c = Circle(pos)
                c.draw(fill=term.green)
            elif val.code == 259:
                c.erase()
                if (pos[1] - 1 - CIRCLE_RADIUS) >= 0: 
                    pos = (pos[0], pos[1] - 1)
                c = Circle(pos)
                c.draw(fill=term.green)
            elif val.code == 258:
                c.erase()
                if (pos[1] + 1 + CIRCLE_RADIUS) <= term.height: 
                    pos = (pos[0], pos[1] + 1)
                c = Circle(pos)
                c.draw(fill=term.green)
        val = term.inkey()
    c.erase()
    c.draw(fill=term.red)
    c.name = get_v_name()
    helper_msg_box.erase()
    return c
    
def add_edge(selection_circles: List[Circle], edges: Dict[str, List[str]]) -> Line:
    """Assumes there exists at least 2 circles"""
    top_msg = \
"""Select two vertices to connect them with an edge
Select using arrow keys and `ENTER`"""
    helper_msg_box = MessageBox('tl', top_msg)
    helper_msg_box.draw()
    first = select_circle(selection_circles, edges)
    first_c = selection_circles[first] 
    first_c.draw(fill=term.green)
    second = select_circle(selection_circles, edges, first)
    second_c = selection_circles[second]
    first_c.erase()
    line = Line(*shortest_points(first_c, second_c))
    line.draw(fill=term.red)
    edges[first_c.name].append(second_c.name)
    edges[second_c.name].append(first_c.name)
    return line

def select_circle(circles: List[Circle], edges: Dict[str, List[str]], first: int = -1) -> int:
    if first != -1 and len(edges[circles[first]]) == len(circles) - 1:
        raise Exception('Your first choice exhausts all choices rip lmao')
    current = 0 
    while (current == first) or (first != -1 and circles[first] in edges[current]):
        current = (current + 1) % len(circles)
    current_c = circles[current]
    current_c.draw(fill=term.green)
    val = term.inkey()
    while not val.is_sequence or val.code != 343:
        if val.is_sequence:
            if val.code == 261 or val.code == 259:
                # up-right
                current = (current + 1) % len(circles)
                while (current == first) or (first != -1 and circles[first] in edges[current]):
                    current = (current + 1) % len(circles)
            elif val.code == 260 or val.code == 258:
                # left-down
                current = (current - 1) % len(circles)
                while (current == first) or (first != -1 and circles[first] in edges[current]):
                    current = (current - 1) % len(circles)
            else:
                continue
            current_c.erase() 
            current_c.draw(fill=term.red)
            current_c = circles[current]
            current_c.draw(fill=term.green)
            val = term.inkey()
    current_c.erase()
    current_c.draw(fill=term.red)
    return current

def get_v_name() -> str:
    i = 0
    while True:
        yield f'v{str(i)}'
        i += 1
