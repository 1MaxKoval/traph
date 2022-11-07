from typing import List, Dict, Tuple
from .graph import Graph
from .ui.ui import set_og_background, TERMINAL as term
from .ui.shapes import MessageBox, Circle, Line, CIRCLE_RADIUS
from .algorithms import shortest_points
from collections import defaultdict

def get_v_name() -> str:
    i = 0
    while True:
        yield f'v{str(i)}'
        i += 1

NAME_GENERATOR = get_v_name()

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
    lines = {}
    edges = defaultdict(list)
    while True:
        with term.cbreak():
            val = ''
            n = len(circles)
            max_edges = (n*(n-1)) // 2
            while val not in {'1', '2', '3', '4', '5'}:
                val = term.inkey()
                if val == '1':
                    menu_box.erase()
                    circles.append(add_vertex())
                    menu_box.draw()
                elif val == '2' and len(circles) >= 1:
                    # BUG: Error while trying to delete a vertex
                    menu_box.erase()
                    remove_vertex(circles, lines, edges)
                    menu_box.draw()
                elif val == '3' and len(circles) >= 2 and len(lines) + 1 <= max_edges:
                    menu_box.erase()
                    add_edge(circles, edges, lines)
                    menu_box.draw()
                elif val == '4' and len(lines) >= 1:
                    menu_box.erase()
                    remove_edge(edges, lines)
                    menu_box.draw()
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
    c.name = next(NAME_GENERATOR)
    helper_msg_box.erase()
    return c
    
def add_edge(selection_circles: List[Circle], edges: Dict[str, List[str]], edge_line: Dict[Tuple[str, str], Line]) -> Line:
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
    edge_line[(first_c.name, second_c.name)] = line
    helper_msg_box.erase()
    return line

def select_circle(circles: List[Circle], edges: Dict[str, List[str]], first: int = -1) -> int:
    if first != -1 and len(edges[circles[first]]) == len(circles) - 1:
        raise Exception('Your first choice exhausts all choices rip lmao')
    current = 0 
    while (current == first) or (first != -1 and circles[first].name in edges[circles[current].name]):
        current = (current + 1) % len(circles)
    current_c = circles[current]
    current_c.draw(fill=term.green)
    val = term.inkey()
    while not val.is_sequence or val.code != 343:
        if val.is_sequence:
            if val.code == 261 or val.code == 259:
                # up-right
                current = (current + 1) % len(circles)
                while (current == first) or (first != -1 and circles[first].name in edges[circles[current].name]):
                    current = (current + 1) % len(circles)
            elif val.code == 260 or val.code == 258:
                # left-down
                current = (current - 1) % len(circles)
                while (current == first) or (first != -1 and circles[first].name in edges[circles[current].name]):
                    current = (current - 1) % len(circles)
            else:
                val = term.inkey()
                continue
            current_c.erase() 
            current_c.draw(fill=term.red)
            current_c = circles[current]
            current_c.draw(fill=term.green)
        val = term.inkey()
    current_c.erase()
    current_c.draw(fill=term.red)
    return current

def remove_vertex(circles: List[Circle], lines: Dict[Tuple[str, str], Line], edges: Dict[str, List[str]]) -> None:
    msg = \
"""Select a vertex to remove
Select using arrow keys and `ENTER`"""
    msg_box = MessageBox('tl', msg)
    msg_box.draw()
    i = 0
    c_c = circles[i]
    c_c.erase()
    c_c.draw(fill=term.green)
    val = term.inkey()
    while not (val.is_sequence and val.code == 343):
        if val.is_sequence:
            # Weird bug when trying to select a circle to delete!
            if val.code == 261 or val.code == 259:
                i = (i + 1) % len(circles)
                c_c.erase()
                c_c.draw(fill=term.red)
                c_c = circles[i]
                c_c.erase()
                c_c.draw(fill=term.green)
            elif val.code == 260 or val.code == 258:
                i = (i - 1) % len(circles)
                c_c.erase()
                c_c.draw(fill=term.red)
                c_c = circles[i]
                c_c.erase()
                c_c.draw(fill=term.green)
        val = term.inkey()
    c_c.erase()
    if c_c.name in edges:
        del edges[c_c.name]
    for name, neighbors in edges.items():
        for i in range(len(neighbors)):
            if neighbors[i] == c_c.name:
                del neighbors[i]
                break
    to_delete = list()
    for tup, line in lines.items():
        if c_c.name in tup:
            to_delete.append(tup)
    for tup in to_delete:
        line = lines[tup]
        line.erase()
        del lines[tup]
        del line
    del circles[i]
    del c_c
    msg_box.erase()

def remove_edge(edges: Dict[str, List[str]], edge_line: Dict[Tuple[str, str], Line]) -> None:
    top_msg = \
"""Select an edge to remove
Select using arrow keys and `ENTER`"""
    msg_box = MessageBox('tl', top_msg)
    msg_box.draw()
    i = 0
    v_to_v = list(edge_line)
    v1, v2 = v_to_v[i]
    c_l = edge_line[(v1, v2)]
    c_l.erase()
    c_l.draw(fill=term.green)
    val = term.inkey()
    while not (val.is_sequence and val.code == 343):
        if val.is_sequence:
            if val.code == 261 or val.code == 259:
                c_l.erase()
                c_l.draw(fill=term.red)
                i = (i + 1) % len(v_to_v)
                v1, v2 = v_to_v[i]
                c_l = edge_line[(v1, v2)]
                c_l.erase()
                c_l.draw(fill=term.green)
            elif val.code == 260 or val.code == 258:
                c_l.erase()
                c_l.draw(fill=term.red)
                i = (i - 1) % len(v_to_v)
                v1, v2 = v_to_v[i]
                c_l = edge_line[(v1, v2)]
                c_l.erase()
                c_l.draw(fill=term.green)
        val = term.inkey()
    del edge_line[(v1, v2)]
    edges[v1].remove(v2)
    edges[v2].remove(v1)
    c_l.erase()
    del c_l
    msg_box.erase()

def run_algorithms() -> None:
    pass
