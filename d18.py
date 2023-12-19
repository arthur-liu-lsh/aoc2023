from collections import deque
from typing import Deque, Dict, List, Set, Tuple

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d18test.txt")
lines = utils.parse("d18.txt")

dir_map = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0)
}

dir_to_int = {
    'R': 0,
    'D': 1,
    'L': 2,
    'U': 3 
}

int_to_dir = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U'
}

def shoelace(world: List[Tuple[int, int]]):
    area = 0
    for k in range(len(world)-1):
        i1, j1 = world[k]
        i2, j2 = world[k+1]
        area += (i1 + i2) * (j1 - j2)
    i1, j1 = world[-1]
    i2, j2 = world[0]
    area += (i1 + i2) * (j1 - j2)
    return int(area // 2)

def resize(world, directions):
    world_resized = []
    turns = []
    for k in range(len(directions) - 1):
        if ((directions[k+1] - directions[k]) % 4) == 1:
            turns.append(True)
        elif ((directions[k+1] - directions[k]) % 4) == 3:
            turns.append(False)

    world_resized.append((-0.5, -0.5))
    for k in range(len(turns)):
        off_i, off_j = 0, 0
        if turns[k]:
            if directions[k] == 0:
                off_i -= 0.5
                off_j += 0.5
            elif directions[k] == 1:
                off_i += 0.5
                off_j += 0.5
            elif directions[k] == 2:
                off_i += 0.5
                off_j -= 0.5
            else:
                off_i -= 0.5
                off_j -= 0.5
        else:
            if directions[k] == 0:
                off_i -= 0.5
                off_j -= 0.5
            elif directions[k] == 1:
                off_i -= 0.5
                off_j += 0.5
            elif directions[k] == 2:
                off_i += 0.5
                off_j += 0.5
            else:
                off_i += 0.5
                off_j -= 0.5
        i, j = world[k+1]
        world_resized.append((i+off_i, j+off_j))
    return world_resized

@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0


    world = []
    world.append((0, 0))
    directions = []
    i = 0
    j = 0
    for line in lines:
        words = line.split()
        direction = dir_map[words[0]]
        di, dj = direction
        distance  = int(words[1])
        i += di * distance
        j += dj * distance
        world.append((i,j))
        directions.append(dir_to_int[words[0]])
    
    world_resized = resize(world, directions)
    result1 = shoelace(world_resized)

    world = []
    directions = []
    world.append((0, 0))
    i, j = 0, 0
    for line in lines:
        words = line.split()
        code = words[2]
        code = code.replace('(#', '')
        code = code.replace(')', '')
        direction = dir_map[int_to_dir[int(code[-1])]]
        directions.append(int(code[-1]))
        di, dj = direction
        distance  = int(code[0:5], 16)
        i += di * distance
        j += dj * distance
        world.append((i,j))

    result2 = shoelace(resize(world, directions))

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run(lines_test)
run(lines)