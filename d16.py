from typing import Dict, List, Set, Tuple

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d16test.txt")
lines = utils.parse("d16.txt")

def propagate_ray(world, lines, i, j, di, dj, already_explored):
    n,m = world.shape
    if (i,j,di,dj) in already_explored:
        return
    already_explored.add((i,j,di,dj))

    while i >= 0 and i < n and j >= 0 and j < m:
        i += di
        j += dj
        if not (i >= 0 and i < n and j >= 0 and j < m):
            break
        world[i,j] = 1
        char = lines[i][j]
        if char != '.':
            if char == '-':
                if di != 0 and dj == 0:
                    propagate_ray(world, lines, i, j, 0, 1, already_explored)
                    propagate_ray(world, lines, i, j, 0, -1, already_explored)
                else:
                    propagate_ray(world, lines, i, j, 0, dj, already_explored)
            elif char == '|':
                if dj != 0 and di == 0:
                    propagate_ray(world, lines, i, j, 1, 0, already_explored)
                    propagate_ray(world, lines, i, j, -1, 0, already_explored)
                else:
                    propagate_ray(world, lines, i, j, di, 0, already_explored)
            elif char == '\\':
                if di != 0 and dj == 0:
                    propagate_ray(world, lines, i, j, 0, di, already_explored)
                elif dj != 0 and di == 0:
                    propagate_ray(world, lines, i, j, dj, 0, already_explored)
            elif char == '/':
                if di != 0 and dj == 0:
                    propagate_ray(world, lines, i, j, 0, -di, already_explored)
                elif dj != 0 and di == 0:
                    propagate_ray(world, lines, i, j, -dj, 0, already_explored)
            break

def propagate_ray_start(world, lines, i, j, di, dj, already_explored):
    world[i,j] = 1
    char = lines[i][j]
    if char != '.':
        if char == '-':
            if di != 0 and dj == 0:
                propagate_ray(world, lines, i, j, 0, 1, already_explored)
                propagate_ray(world, lines, i, j, 0, -1, already_explored)
            else:
                propagate_ray(world, lines, i, j, 0, dj, already_explored)
        elif char == '|':
            if dj != 0 and di == 0:
                propagate_ray(world, lines, i, j, 1, 0, already_explored)
                propagate_ray(world, lines, i, j, -1, 0, already_explored)
            else:
                propagate_ray(world, lines, i, j, di, 0, already_explored)
        elif char == '\\':
            if di != 0 and dj == 0:
                propagate_ray(world, lines, i, j, 0, di, already_explored)
            elif dj != 0 and di == 0:
                propagate_ray(world, lines, i, j, dj, 0, already_explored)
        elif char == '/':
            if di != 0 and dj == 0:
                propagate_ray(world, lines, i, j, 0, -di, already_explored)
            elif dj != 0 and di == 0:
                propagate_ray(world, lines, i, j, -dj, 0, already_explored)
    else:
        propagate_ray(world, lines, i, j, di, dj, already_explored)

@utils.measure
def run(lines: List[str]):
    
    result1 = 0
    result2 = 0
    
    n = len(lines)
    m = len(lines[0])

    world = np.zeros((n, m))
    already_explored = set()

    propagate_ray_start(world, lines, 0, 0, 0, 1, already_explored)

    result1 = int(world.sum())

    best_count = 0

    for i in range(n):
        world = np.zeros((n, m))
        already_explored = set()
        propagate_ray_start(world, lines, i, 0, 0, 1, already_explored)
        best_count = max(best_count, world.sum())
    for i in range(n):
        world = np.zeros((n, m))
        already_explored = set()
        propagate_ray_start(world, lines, i, m-1, 0, -1, already_explored)
        best_count = max(best_count, world.sum())
    for j in range(m):
        world = np.zeros((n, m))
        already_explored = set()
        propagate_ray_start(world, lines, 0, j, 1, 0, already_explored)
        best_count = max(best_count, world.sum())
    for j in range(m):
        world = np.zeros((n, m))
        already_explored = set()
        propagate_ray_start(world, lines, n-1, j, -1, 0, already_explored)
        best_count = max(best_count, world.sum())

    result2 = int(best_count)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')


run(lines_test)
run(lines)