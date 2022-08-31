from collections import defaultdict
from typing import List, Tuple
import pprint

class Graph:

    def __init__(self, vertices: List[str], edges: List[Tuple[str, str]]):
        # TODO: Add input validation (maybe in another place lmao)
        # Assumes unique vertex names (sort of)
        self.v = vertices
        self.e = edges
        self.n = defaultdict(list)
        # Assumes bidirectional relationship + repetitions are allowed
        for edge in edges:
            self.n[edge[0]].append(edge[1])
            self.n[edge[1]].append(edge[0])

    def __repr__(self) -> str:
        return pprint.pformat(self.n)

    def __str__(self):
        pass