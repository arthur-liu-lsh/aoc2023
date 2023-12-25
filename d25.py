from collections import deque
from typing import Deque, Dict, List, Set, Tuple
import re

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

lines_test = utils.parse("d25test.txt")
lines = utils.parse("d25.txt")

@utils.measure
def run(lines: List[str]):

    result = 0
    
    graph = nx.Graph()

    for line in lines:
        words = line.split()
        targets = words[1:]
        origin = words[0][0:-1]
        for target in targets:
            if origin not in graph:
                graph.add_node(origin)
            if target not in graph:
                graph.add_node(target)
            graph.add_edge(origin, target)
            graph.add_edge(target, origin)

    edges_to_remove = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(edges_to_remove)

    result = 1
    for sub_graph in nx.connected_components(graph):
        result *= len(sub_graph)

    print(f'Result: {result}')

run(lines_test)
run(lines)
