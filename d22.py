from collections import deque
from typing import Deque, Dict, List, Set, Tuple
from math import lcm

from copy import deepcopy

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import re

lines_test = utils.parse("d22test.txt")
lines = utils.parse("d22.txt")

line_re = re.compile(r'^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)$')

def above_bricks(brick, bricks):
    res = set()
    z = max(brick[2], brick[5])+1
    x_min = min(brick[0], brick[3])
    x_max = max(brick[0], brick[3])
    y_min = min(brick[1], brick[4])
    y_max = max(brick[1], brick[4])
    for other_brick in bricks:
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                if brick_contains(other_brick, x, y, z):
                    res.add(other_brick)
    return res

def below_bricks(brick, bricks, world = None, distance = 1):
    res = set()
    z = min(brick[2], brick[5])-distance
    x_min = min(brick[0], brick[3])
    x_max = max(brick[0], brick[3])
    y_min = min(brick[1], brick[4])
    y_max = max(brick[1], brick[4])
    if world is None:
        for other_brick in bricks:
            for x in range(x_min, x_max+1):
                for y in range(y_min, y_max+1):
                    if brick_contains(other_brick, x, y, z):
                        res.add(other_brick)
    else:
        for x in range(x_min, x_max+1):
            for y in range(y_min, y_max+1):
                if (x,y,z) in world:
                    res.add((x,y,z))
    return res

def brick_contains(brick, x, y, z):
    x_min = min(brick[0], brick[3])
    x_max = max(brick[0], brick[3])
    y_min = min(brick[1], brick[4])
    y_max = max(brick[1], brick[4])
    z_min = min(brick[2], brick[5])
    z_max = max(brick[2], brick[5])
    if x not in range(x_min, x_max+1):
        return False
    if y not in range(y_min, y_max+1):
        return False
    if z not in range(z_min, z_max+1):
        return False
    return True

def can_remove(brick, bricks):
    above = above_bricks(brick, bricks)
    if len(above) == 0:
        return True
    for b in above:
        if len(below_bricks(b, bricks)) == 1:
            return False
    return True

def world_remove(world, brick):
    x_min = min(brick[0], brick[3])
    x_max = max(brick[0], brick[3])
    y_min = min(brick[1], brick[4])
    y_max = max(brick[1], brick[4])
    z_min = min(brick[2], brick[5])
    z_max = max(brick[2], brick[5])
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            for z in range(z_min, z_max+1):
                world.remove(((x,y,z)))

def world_add(world, brick):
    x_min = min(brick[0], brick[3])
    x_max = max(brick[0], brick[3])
    y_min = min(brick[1], brick[4])
    y_max = max(brick[1], brick[4])
    z_min = min(brick[2], brick[5])
    z_max = max(brick[2], brick[5])
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            for z in range(z_min, z_max+1):
                world.add(((x,y,z)))

def fall_bricks(bricks):
    moved = True
    iter = 0
    while moved:
        moved = False
        new_bricks = set()
        world = set()
        for brick in bricks:
            world_add(world, brick)
        for brick in bricks:
            z_min = min(brick[2], brick[5])
            if z_min == 1:
                new_bricks.add(brick)
            else:
                distance = 1
                while distance < 1000:
                    if len(below_bricks(brick, bricks, world, distance)) > 0:
                        new_bricks.add((brick[0], brick[1], brick[2]-(distance-1), brick[3], brick[4], brick[5]-(distance-1)))
                        break
                    elif z_min - distance < 1:
                        new_bricks.add((brick[0], brick[1], brick[2]-(distance-1), brick[3], brick[4], brick[5]-(distance-1)))
                        break
                    else:
                        moved = True
                    distance += 1

        bricks = new_bricks
        iter+=1
    return bricks


@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0

    n = len(lines)

    bricks = set()

    for line in lines:
        groups = line_re.match(line).groups()
        bricks.add(tuple([int(elem) for elem in groups]))

    bricks = fall_bricks(bricks)

    for brick in bricks:
        if can_remove(brick, bricks):
            result1 += 1

    i = 0
    for brick in bricks:
        print(i)
        world = set()
        for b in bricks:
            world_add(world, b)
        moved = set()
        queue = deque()
        queue.append(brick)
        while len(queue) > 0:
            current_brick = queue.popleft()
            world_remove(world, current_brick)
            for a in above_bricks(current_brick, bricks):
                if len(below_bricks(a, bricks, world)) == 0:
                    moved.add(a)
                    queue.append(a)
        result2 += len(moved)
        i += 1

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')




run(lines_test)
run(lines)
