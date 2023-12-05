from typing import List, Tuple
import utils
import re
from functools import cache
from numba import njit
import numpy as np

lines = utils.parse("d5.txt")

@njit
def apply_map(value, destination, start, diff):
    if value in range(start, start+diff):
        return destination + value - start
    else:
        return None

def apply_maps(seed: int, mappings: List[List[List[int]]]):
    for mapping in mappings:
        mapping = np.array(mapping)
        for start, destination, diff in mapping:
            value = apply_map(seed, start, destination, diff)
            if value != None:
                seed = value
                break
    return seed

def apply_maps_all(seed_range: Tuple[int, int], mappings: List[List[List[int]]]):
    minimum = None
    for seed in range(seed_range[0], seed_range[0]+seed_range[1]):
        for mapping in mappings:
            for start, destination, diff in mapping:
                value = apply_map(seed, start, destination, diff)
                if value != None:
                    seed = value
                    break
        if minimum is None:
            minimum = seed
        else:
            minimum = min(seed, minimum)

@utils.measure
def run():

    seeds = []
    mappings = []

    for i, line in enumerate(lines):
        if i == 0:
            words = line.split()
            seeds = [int(word) for word in words[1:]]
        elif line == '':
            mappings.append([])
        else:
            if any(char.isdigit() for char in line):
                words = line.split()
                words = [int(word) for word in words]
                mappings[-1].append(words)



    outputs = []

    for i, seed in enumerate(seeds):
        for mapping in mappings:
            for start, destination, diff in mapping:
                value = apply_map(seed, start, destination, diff)
                if value != None:
                    seed = value
                    break
            if i == 1:
                print(seed)
        outputs.append(seed)
    
    result1 = min(outputs)

    print(f'Part 1: {result1}')

run()