from collections import defaultdict
from typing import List, Tuple
import pprint

class GraphError(Exception):
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

class Graph:

    def __init__(self, vertices: List[str], edges: List[Tuple[str, str]], positions: List[Tuple[int,int]] = None):
        if positions is None:
            positions = []
        if len(positions) != len(vertices):
            raise GraphError('Number of vertices is not the same as bla bla..')
        # TODO: Add input validation (maybe in another place lmao)
        # Assumes unique vertex names (sort of)
        self.v = vertices
        self.positions = positions
        self.e = edges
        self.n = defaultdict(list)
        self.v_e = defaultdict(list)
        # Assumes bidirectional relationship + edge repetitions are allowed
        for i, edge in enumerate(edges):
            # Create node - edge mapping
            self.v_e[edge[0]].append(i)
            self.v_e[edge[1]].append(i)
            # Create node - node mapping
            self.n[edge[0]].append(edge[1])
            self.n[edge[1]].append(edge[0])

    def __repr__(self) -> str:
        return str(self.n)

    def __str__(self):
        pass