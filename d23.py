from collections import deque
from typing import Deque, Dict, List, Set, Tuple
import sys
sys.setrecursionlimit(1000000)

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d23test.txt")
lines = utils.parse("d23.txt")


def neighbours(lines, i, j, n, m):
    adj = []
    if lines[i][j] == '.':
        if (i < n-1) and lines[i+1][j] not in '#^':
            adj.append((i+1,j))
        if (i > 0) and lines[i-1][j] not in '#v':
            adj.append((i-1,j))
        if (j < m-1) and lines[i][j+1] not in '#<':
            adj.append((i,j+1))
        if (j > 0) and lines[i][j-1] not in '#>':
            adj.append((i,j-1))
    elif lines[i][j] == '>':
        if (j < m-1) and lines[i][j+1] != '#':
            adj.append((i,j+1))
    elif lines[i][j] == '<':
        if (j > 0) and lines[i][j-1] != '#':
            adj.append((i,j-1))
    elif lines[i][j] == '^':
        if (i > 0) and lines[i-1][j] != '#':
            adj.append((i-1,j))
    elif lines[i][j] == 'v':
        if (i < n-1) and lines[i+1][j] != '#':
            adj.append((i+1,j))
    return adj

def neighbours2(lines, i, j, n, m):
    adj = []
    if (i < n-1) and lines[i+1][j] != '#':
        adj.append((i+1,j))
    if (i > 0) and lines[i-1][j] != '#':
        adj.append((i-1,j))
    if (j < m-1) and lines[i][j+1] != '#':
        adj.append((i,j+1))
    if (j > 0) and lines[i][j-1] != '#':
        adj.append((i,j-1))
    return adj

def find_nodes(lines, startpos, n, m):
    queue = deque()
    queue.append((startpos))
    distances = -1 * np.ones((n, m), np.int64)
    distances[startpos] = 0
    nodes = []
    while len(queue) > 0:
        i, j = queue.popleft()
        adj = neighbours2(lines, i, j, n, m)
        for ii, jj in adj:
            if distances[ii, jj] == -1:
                distances[ii, jj] = distances[i, j] + 1
                if len(neighbours2(lines, ii, jj, n, m)) > 2 or (ii, jj) in [(0, 1), (n-1, m-2)]:
                    nodes.append(((ii, jj), distances[ii, jj]))
                else:
                    queue.append((ii, jj))
    return nodes

def build_graph(lines):
    n = len(lines)
    m = len(lines[0])

    startpos = (0, 1)

    queue = deque()
    queue.append(startpos)

    distances = {}
    graph = {}

    while len(queue) > 0:
        curr_coords = queue.popleft()
        adj = find_nodes(lines, curr_coords, n, m)
        for coords, distance in adj:
            distances[(curr_coords, coords)] = distance
            distances[(coords, curr_coords)] = distance
            if coords not in graph:
                queue.append((coords))
        graph[curr_coords] = [coords for coords, _ in adj]
    return graph, distances



@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0

    n = len(lines)
    m = len(lines[0])

    for i, line in enumerate(lines):
        lines[i] = tuple(line)

    lines = tuple(lines)

    graph, distances = build_graph(lines)
    result1 = dfs(lines, (0, 1), n, m, frozenset())
    result2 = dfs2(lines, (0, 1), n, m, frozenset(), graph, distances)


    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

def dfs(lines, startpos, n, m, visited):
    if startpos == (n-1, m-2):
        return 0
    visited = set(visited)
    visited.add(startpos)
    visited = frozenset(visited)
    adj = neighbours(lines, startpos[0], startpos[1], n, m)
    if len(adj) == 0:
        return -1000000000
    distance = -1000000
    for i, j in adj:
        if (i, j) in visited:
            continue
        eval = 1 + dfs(lines, (i, j), n, m, visited)
        distance = max(eval, distance)
    return distance

def dfs2(lines, startpos, n, m, visited, graph, distances):
    if startpos == (n-1, m-2):
        return 0
    visited = set(visited)
    visited.add(startpos)
    visited = frozenset(visited)
    adj = graph[startpos]
    if len(adj) == 0:
        return -1000000000
    distance = -1000000
    for coords in adj:
        if coords in visited:
            continue
        eval = distances[(startpos, coords)] + dfs2(lines, coords, n, m, visited, graph, distances)
        distance = max(eval, distance)
    return distance




run(lines_test)
run(lines)
