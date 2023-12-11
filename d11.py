from collections import deque
from typing import List, Tuple
import utils
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d11test.txt")
lines = utils.parse("d11.txt")

def hamming(pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2
    return abs(i1 - i2) + abs(j1 - j2)

def domain_expansion(galaxies, to_expand_vertical, to_expand_horizontal, expand_size):
    expand_sizes_vertical = [0 for _ in galaxies]
    expand_sizes_horizontal = [0 for _ in galaxies]
    for elem in to_expand_vertical:
        for k in range(len(galaxies)):
            i, j = galaxies[k]
            if i > elem:
                expand_sizes_vertical[k] += expand_size
    for elem in to_expand_horizontal:
        for k in range(len(galaxies)):
            i, j = galaxies[k]
            if j > elem:
                expand_sizes_horizontal[k] += expand_size

    galaxies_new = []

    for k in range(len(galaxies)):
        i,j = galaxies[k]
        i += expand_sizes_vertical[k]
        j += expand_sizes_horizontal[k]
        galaxies_new.append((i,j))

    return galaxies_new

@utils.measure
def run(lines: List[str]):

    n, m = len(lines), len(lines[0])

    galaxies = []

    world = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            if lines[i][j] == '#':
                world[i,j] = 1
                galaxies.append((i,j))

    to_expand_vertical = []
    to_expand_horizontal = []

    for i in range(n):
        if np.sum(world[i]) == 0:
            to_expand_vertical.append(i)

    world = world.transpose()

    for i in range(n):
        if np.sum(world[i]) == 0:
            to_expand_horizontal.append(i)

    to_expand_vertical.reverse()
    to_expand_horizontal.reverse()

    world = world.transpose()

    # plt.figure()
    # plt.spy(world)
    # plt.show()


    n,m = world.shape

    galaxies1 = domain_expansion(galaxies, to_expand_vertical, to_expand_horizontal, 1)
    galaxies2 = domain_expansion(galaxies, to_expand_vertical, to_expand_horizontal, 999999)

    result1 = 0
    done = set()

    for galaxy1 in galaxies1:
        for galaxy2 in galaxies1:
            if ((galaxy1, galaxy2) not in done) and ((galaxy2, galaxy1) not in done):
                result1 += hamming(galaxy1, galaxy2)
                done.add((galaxy1, galaxy2))
    
    result2 = 0
    done = set()

    for galaxy1 in galaxies2:
        for galaxy2 in galaxies2:
            if ((galaxy1, galaxy2) not in done) and ((galaxy2, galaxy1) not in done):
                result2 += hamming(galaxy1, galaxy2)
                done.add((galaxy1, galaxy2))


    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run(lines_test)
run(lines)