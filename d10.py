from collections import deque
from typing import List, Tuple
import utils
import numpy as np
import matplotlib.pyplot as plt

lines_test = utils.parse("d10test.txt")
lines = utils.parse("d10.txt")

char_to_connect = {
    '|': (0, 0, 1, 1),
    '-': (1, 1, 0, 0),
    'L': (0, 1, 1, 0),
    'J': (1, 0, 1, 0),
    '7': (1, 0, 0, 1),
    'F': (0, 1, 0, 1),
    '.': (0, 0, 0, 0),
    'S': (1, 1, 1, 1)
}

def start_propagate(pos: Tuple[int, int], lines: List[str], distances: List[int]) -> List[Tuple[int, int]]:
    i, j = pos
    neighbours = []
    if j > 0:
        if char_to_connect[lines[i][j-1]][1]:
            neighbours.append((i,j-1))
            distances[i][j-1] = 1
    if j < len(lines[i]) - 1:
        if char_to_connect[lines[i][j+1]][0]:
            neighbours.append((i,j+1))
            distances[i][j+1] = 1
    if i > 0:
        if char_to_connect[lines[i-1][j]][3]:
            neighbours.append((i-1,j))
            distances[i-1][j] = 1
    if i < len(lines) - 1:
        if char_to_connect[lines[i+1][j]][2]:
            neighbours.append((i+1,j))
            distances[i+1][j] = 1
    return neighbours

def propagate(pos: Tuple[int, int], lines: List[List[str]], distances: List[int]) -> List[Tuple[int, int]]:
    i, j = pos
    directions = char_to_connect[lines[i][j]]
    current_distance = distances[i][j]
    neighbours = []
    if directions[0] and j > 0:
        if distances[i][j-1] == 0 or distances[i-1][j] > current_distance:
            neighbours.append((i,j-1))
            distances[i][j-1] = current_distance + 1
    if directions[1] and j < len(lines[i]) - 1:
        if distances[i][j+1] == 0 or distances[i][j+1] > current_distance:
            neighbours.append((i,j+1))
            distances[i][j+1] = current_distance + 1
    if directions[2] and i > 0:
        if distances[i-1][j] == 0 or distances[i-1][j] > current_distance:
            neighbours.append((i-1,j))
            distances[i-1][j] = current_distance + 1
    if directions[3] and i < len(lines) - 1:
        if distances[i+1][j] == 0 or distances[i+1][j] > current_distance:
            neighbours.append((i+1,j))
            distances[i+1][j] = current_distance + 1

    return neighbours


def start_fill_map(pos: Tuple[int, int], lines: List[str]) -> List[Tuple[int, int]]:
    i, j = pos
    neighbours = []
    if j > 0:
        if char_to_connect[lines[i][j-1]][1]:
            neighbours.append((i,j-1))
    if j < len(lines[i]) - 1:
        if char_to_connect[lines[i][j+1]][0]:
            neighbours.append((i,j+1))
    if i > 0:
        if char_to_connect[lines[i-1][j]][3]:
            neighbours.append((i-1,j))
    if i < len(lines) - 1:
        if char_to_connect[lines[i+1][j]][2]:
            neighbours.append((i+1,j))
    return neighbours

def fill_map_loop(pos: Tuple[int, int], lines: List[List[str]], big_map: List[List[int]]) -> List[Tuple[int, int]]:
    i, j = pos
    directions = char_to_connect[lines[i][j]]
    neighbours = []
    if directions[0] and j > 0:
        if big_map[i*2+1][(j-1)*2 + 1] == 0:
            neighbours.append((i,j-1))
        big_map[i*2+1][(j-1)*2+1] = 1
        big_map[i*2+1][j*2-1+1] = 1
    if directions[1] and j < len(lines[i]) - 1:
        if big_map[i*2+1][(j+1)*2+1] == 0:
            neighbours.append((i,j+1))
        big_map[i*2+1][(j+1)*2+1] = 1
        big_map[i*2+1][j*2+1+1] = 1
    if directions[2] and i > 0:
        if big_map[(i-1)*2+1][j*2+1] == 0:
            neighbours.append((i-1,j))
        big_map[(i-1)*2+1][j*2+1] = 1
        big_map[i*2-1+1][j*2+1] = 1
    if directions[3] and i < len(lines) - 1:
        if big_map[(i+1)*2+1][j*2+1] == 0:
            neighbours.append((i+1,j))
        big_map[(i+1)*2+1][j*2+1] = 1
        big_map[i*2+1+1][j*2+1] = 1

    return neighbours

def fill_map(pos: Tuple[int, int], big_map: List[List[int]]) -> List[Tuple[int, int]]:
    i, j = pos
    n, m = len(big_map), len(big_map[0])
    neighbours = []
    if j > 0:
        if big_map[i][j-1] == 0:
            big_map[i][j-1] = -1
            neighbours.append((i, j-1))
    if j < m - 1:
        if big_map[i][j+1] == 0:
            big_map[i][j+1] = -1
            neighbours.append((i,j+1))
    if i > 0:
        if big_map[i-1][j] == 0:
            big_map[i-1][j] = -1
            neighbours.append((i-1,j))
    if i < n - 1:
        if big_map[i+1][j] == 0:
            big_map[i+1][j] = -1
            neighbours.append((i+1,j))
    return neighbours

@utils.measure
def run(lines: List[str]):

    n, m = len(lines), len(lines[0])

    distances = [[0 for j in range(m)] for i in range(n)]

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == 'S':
                distances[i][j] = -1
                startpos = (i,j)

    queue = deque()
    queue += start_propagate(startpos, lines, distances)
    while len(queue) > 0:
        pos = queue.popleft()
        queue += propagate(pos, lines, distances)

    result1 = max([max(line) for line in distances])
    
    big_map = [[0 for j in range(m * 2 + 1)] for i in range(n * 2 + 1)]

    queue = deque()
    queue += start_fill_map(startpos, lines)
    while len(queue) > 0:
        pos = queue.popleft()
        queue += fill_map_loop(pos, lines, big_map)

    queue = deque()
    queue.append((0, 0))
    while len(queue) > 0:
        pos = queue.popleft()
        queue += fill_map(pos, big_map)

    result2 = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if big_map[i*2+1][j*2+1] == 0:
                result2 += 1

    # plt.figure()
    # plt.imshow([line[1::2] for line in big_map[1::2]])
    # plt.show()

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run(lines_test)
run(lines)