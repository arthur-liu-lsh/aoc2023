from typing import List, Tuple
import utils
import re
from functools import cache
from numba import njit
import numpy as np

lines = utils.parse("d6.txt")

@utils.measure
def run():

    seeds = []
    mappings = []

    times = [int(elem) for elem in (lines[0].split()[1:])]
    distances = [int(elem) for elem in (lines[1].split()[1:])]

    n = len(times)
    counts = []

    for i in range(n):
        time = times[i]
        count = 0
        for j in range(time):
            distance = (time-j) * j
            if distance > distances[i]:
                count+=1
        counts.append(count)
    
    result1 = 1
    for elem in counts:
        result1 *= elem

    times2 = int("".join(lines[0].split()[1:]))
    distances2 = int("".join(lines[1].split()[1:]))

    n = len(times)
    counts = []

    count = 0
    for j in range(times2):
        distance = (times2-j) * j
        if distance > distances2:
            count+=1
    counts.append(count)
    
    result2 = 1
    for elem in counts:
        result2 *= elem


    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run()