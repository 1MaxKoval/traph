from typing import List, Dict
from .graph import Graph
from .ui.ui import set_og_background, TERMINAL as term
from .ui.shapes import MessageBox, Circle, Line, CIRCLE_RADIUS


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
    edges = {}
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
                    lines.append(add_edge(circles))
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
    
def add_edge(selection_circles: List[Circle]) -> Line:
    """Assumes there exists at least 2 circles"""
    top_msg = \
"""Select two vertices to connect them with an edge
Select using arrow keys and `ENTER`"""
    helper_msg_box = MessageBox('tl', top_msg)
    helper_msg_box.draw()

def select_circle(start: int, circles: List[Circle], edges: Dict[str, List[str]], first = '') -> int:
    # TODO: Add bidrectional relationship to edges dictionary
    if start < 0 or start >= len(circles):
        raise Exception(f'{start} outside of circles list bounds')
    current = start
    start_circle = circles[start]
    start_circle.erase()
    start_circle.draw(fill=term.green)
    val = term.inkey()
    while not val.is_sequence() or val.code != 343:
        if val.code == '261' or val.code == '259':
            current = (current + 1) % len(circles)
            # TODO: Carry on with this later!
            while (current == start) or (first and first in edges[current]):
                current = (current + 1) % len(circles)
        elif val.code == '260' or val.code == '258':
            # left-down
            pass
        val = term.inkey()
    pass

def get_v_name() -> str:
    i = 0
    while True:
        yield f'v{str(i)}'

def get_next_valid_circle(circles):
    pass