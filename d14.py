from typing import List, Tuple

import numpy as np
import utils
import functools

lines_test = utils.parse("d14test.txt")
lines = utils.parse("d14.txt")

def tilt(state_move: set, state_fixed: set, n: int, m: int, direction: int):
    if direction == 0:
        di = -1
        dj = 0
    elif direction == 1:
        di = 0
        dj = -1
    elif direction == 2:
        di = 1
        dj = 0
    elif direction == 3:
        di = 0
        dj = 1
    moved = True
    while moved:
        moved = False
        for i,j in state_move:
            pos = i,j
            new_pos = i+di, j+dj
            if new_pos[0] < 0:
                continue
            if new_pos[1] < 0:
                continue
            if new_pos[0] >= n:
                continue
            if new_pos[1] >= m:
                continue
            if new_pos not in state_fixed and new_pos not in state_move:
                state_move.remove(pos)
                state_move.add(new_pos)
                moved = True
    return state_move

@functools.cache
def tilt_cycle(state_move: frozenset, state_fixed: set, n: int, m: int):
    state_move = set(state_move)
    state_move = tilt(state_move, state_fixed, n, m, 0)
    state_move = tilt(state_move, state_fixed, n, m, 1)
    state_move = tilt(state_move, state_fixed, n, m, 2)
    state_move = tilt(state_move, state_fixed, n, m, 3)
    return frozenset(state_move)


def count_points(state_move, n):
    count = 0
    for i, _ in state_move:
        count += n-i
    return count

@utils.measure
def run(lines: List[str]):
    
    result1 = 0
    result2 = 0

    n = len(lines)
    m = len(lines[0])

    state_move = set()
    state_fixed = set()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                state_fixed.add((i,j))
            elif char == 'O':
                state_move.add((i,j))

    state_move = tilt(state_move, state_fixed, n, m, 0)
    result1 = count_points(state_move, n)

    state_move = set()
    state_fixed = set()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                state_fixed.add((i,j))
            elif char == 'O':
                state_move.add((i,j))


    states = {}
    for k in range(1000000000):
        state_start = frozenset(state_move)
        if state_start in states:
            len_cycle = k - states[state_start]
            if (1000000000 - k) % len_cycle == 0:
                print(count_points(state_move, n))
                break
        states[state_start] = k

        state_move = tilt(state_move, state_fixed, n, m, 0)
        state_move = tilt(state_move, state_fixed, n, m, 1)
        state_move = tilt(state_move, state_fixed, n, m, 2)
        state_move = tilt(state_move, state_fixed, n, m, 3)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')


run(lines_test)
run(lines)