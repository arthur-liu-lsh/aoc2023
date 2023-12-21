from collections import deque
from typing import Deque, Dict, List, Set, Tuple
from math import lcm

from copy import deepcopy

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import re

lines_test = utils.parse("d21test.txt")
lines = utils.parse("d21.txt")


def neighbours(array, i, j, n, m):
    adj = []
    if (i < n-1) and array[(i+1,j)] != 1:
        adj.append((i+1,j))
    if (i > 0) and array[(i-1,j)] != 1:
        adj.append((i-1,j))
    if (j < m-1) and array[(i,j+1)] != 1:
        adj.append((i,j+1))
    if (j > 0) and array[(i,j-1)] != 1:
        adj.append((i,j-1))
    return adj

def neighbours2(array, i, j, n, m):
    adj = []
    if array[((i+1)%n,j)] != 1:
        adj.append(((i+1)%n,j))
    if array[((i-1)%n,j)] != 1:
        adj.append(((i-1)%n,j))
    if array[(i,(j+1)%m)] != 1:
        adj.append((i,(j+1)%m))
    if array[(i,(j-1)%m)] != 1:
        adj.append((i,(j-1)%m))
    return adj

def hamming(i1,j1,i2,j2):
    return abs(i1-i2) + abs(j1-j2)

@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0

    n = len(lines)
    m = len(lines[0])

    world = np.zeros((n,m))

    startpos = None

    for i in range(n):
        for j in range(m):
            if lines[i][j] == '#':
                world[i,j] = 1
            elif lines[i][j] == 'S':
                startpos = (i,j)

    coords = set()
    coords.add(startpos)

    for _ in range(64):
        new_coords = set()
        for i,j in coords:
            for ii,jj in neighbours(world, i, j, n, m):
                new_coords.add((ii,jj))
        coords = new_coords
    result1 = len(coords)

    coords = dict()
    coords[startpos] = 1

    # for _ in range(10):
    #     new_coords = dict()
    #     for i, j in coords:
    #         for ii, jj in neighbours2(world, i, j, n, m):
    #             if hamming(i, j, ii, jj) == 1:
    #                 if (ii, jj) not in new_coords:
    #                     new_coords[(ii, jj)] = coords[(i,j)]
    #             else:
    #                 if (ii, jj) not in new_coords:
    #                     new_coords[(ii, jj)] = coords[(i,j)]
    #                 else:
    #                     new_coords[((ii, jj))] += coords[(i,j)]
    #     coords = new_coords
    #     print(sum(coords.values()))
    # result2 = sum(coords.values())



    plt.figure()
    plt.imshow(world)
    plt.scatter([i for i, j in new_coords], [j for i, j in new_coords])
    plt.show()

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

# run(lines_test)
run(lines)