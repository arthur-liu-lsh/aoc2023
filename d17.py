from collections import deque
from typing import Deque, Dict, List, Set, Tuple

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d17test.txt")
lines = utils.parse("d17.txt")

@functools.cache
def get_neighbours(world, i, j, last_direction, p2 = False):
    neighbours = []
    n = len(world)
    m = len(world[0])
    if p2:
        for ii in range(3, 10):
            new_i = i + ii + 1
            if new_i < n and last_direction not in (1, 3):
                neighbours.append(((new_i, j), measure(world, i, j, new_i, j), 3, abs(new_i - i)-1))
            new_i = i - ii - 1
            if new_i >= 0 and last_direction not in (1, 3):
                neighbours.append(((new_i, j), measure(world, i, j, new_i, j), 1, abs(new_i - i)-1))
        for jj in range(3, 10):
            new_j = j - jj - 1
            if new_j >= 0 and last_direction not in (0, 2):
                neighbours.append(((i, new_j), measure(world, i, j, i, new_j), 2, abs(new_j - j)-1))
            new_j = j + jj + 1
            if new_j < m and last_direction not in (0, 2):
                neighbours.append(((i, new_j), measure(world, i, j, i, new_j), 0, abs(new_j - j)-1))
    else:
        for ii in range(3):
            new_i = i + ii + 1
            if new_i < n and last_direction not in (1, 3):
                neighbours.append(((new_i, j), measure(world, i, j, new_i, j), 3, abs(new_i - i)-1))
            new_i = i - ii - 1
            if new_i >= 0 and last_direction not in (1, 3):
                neighbours.append(((new_i, j), measure(world, i, j, new_i, j), 1, abs(new_i - i)-1))
        for jj in range(3):
            new_j = j - jj - 1
            if new_j >= 0 and last_direction not in (0, 2):
                neighbours.append(((i, new_j), measure(world, i, j, i, new_j), 2, abs(new_j - j)-1))
            new_j = j + jj + 1
            if new_j < m and last_direction not in (0, 2):
                neighbours.append(((i, new_j), measure(world, i, j, i, new_j), 0, abs(new_j - j)-1))
    return tuple(neighbours)

@functools.cache
def measure(world, i1, j1, i2, j2):
    distance = 0
    if i1 == i2:
        for k in range(j1, j2):
            distance += world[i1][k+1]
        for k in range(j2, j1):
            distance += world[i1][k]
    if j1 == j2:
        for k in range(i1, i2):
            distance += world[k+1][j1]
        for k in range(i2, i1):
            distance += world[k][j1]
    return distance

def dijkstra(world, i, j, p2 = False):

    n = len(world)
    m = len(world[0])
    distances = np.ones((n, m, 4), dtype=np.int64) * 1000000
    distances[i, j, 0] = 0
    distances[i, j, 1] = 0
    distances[i, j, 2] = 0
    distances[i, j, 3] = 0
    done = np.zeros((n,m,4), dtype=np.int64)

    # closest = np.zeros((n,m,d,3))
    iter = 0
    while iter < n*m*4:
        current_vertex = None
        min_dis = 1000000000
        for i in range(n):
            for j in range(m):
                for d in range(4):
                    if not done[i,j,d]:
                        if distances[i,j,d] < min_dis:
                            current_vertex = i, j, d
                            min_dis = distances[i,j,d]
        iter+=1
        done[*current_vertex] = 1
        neighbours = get_neighbours(world, *current_vertex, p2)
        for neighbour in neighbours:
            neighbour_coords, neighbour_distance, direction, nodes = neighbour
            if done[*neighbour_coords, direction]:
                continue
            distance = 1000000000
            for k in range(4):
                if k != direction:
                    distance = min(distance, distances[*current_vertex[0:2], k] + neighbour_distance)
            if distance < distances[*neighbour_coords, direction]:
                distances[*neighbour_coords, direction] = distance

    return min(distances[n-1, m-1])

@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0
    
    n = len(lines)
    m = len(lines[0])

    world = np.zeros((n,m), dtype=np.int64)

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            world[i,j] = int(char)
    new_world = []
    for i, _ in enumerate(lines):
        new_world.append(tuple(world[i]))
    world = tuple(new_world)

    result1 = dijkstra(world, 0, 0, p2 = False)
    result2 = dijkstra(world, 0, 0, p2 = True)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')


run(lines_test)
run(lines)