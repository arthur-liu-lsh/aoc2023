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
    if array[((i+1)%n,j%m)] != 1:
        adj.append((i+1,j))
    if array[((i-1)%n,j%m)] != 1:
        adj.append((i-1,j))
    if array[(i%n,(j+1)%m)] != 1:
        adj.append((i,j+1))
    if array[(i%n,(j-1)%m)] != 1:
        adj.append((i,j-1))
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

    coords = set()
    coords.add(startpos)

    X = []
    Y = []

    print(startpos)

    for _ in range(65):
        new_coords = set()
        for i,j in coords:
            for ii,jj in neighbours2(world, i, j, n, m):
                new_coords.add((ii,jj))
        coords = new_coords

    for iter in range(1, 4):
        for _ in range(131):
            new_coords = set()
            for i,j in coords:
                for ii,jj in neighbours2(world, i, j, n, m):
                    new_coords.add((ii,jj))
            coords = new_coords
        X.append(iter)
        Y.append(len(coords))

    k = (26501365 - 65) // 131
    model = np.poly1d(np.polyfit(X, Y, 2))

    result2 = round(model(k))

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

# run(lines_test)
run(lines)
