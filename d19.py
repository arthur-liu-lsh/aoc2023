from collections import deque
from typing import Deque, Dict, List, Set, Tuple

from copy import deepcopy

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import re

lines_test = utils.parse("d19test.txt")
lines = utils.parse("d19.txt")

to_idx = {
    'x':0,
    'm':1,
    'a':2,
    's':3
}



@utils.measure
def run(lines: List[str]):

    result1 = 0
    result2 = 0

    regex = re.compile(r'(.*)\{(.*)\}')
    regex2 = re.compile(r'\{x=(.*),m=(.*),a=(.*),s=(.*)\}')
    rules = {}
    values = []

    switch = False
    for line in lines:
        if line == '':
            switch = True
        else:
            if not switch:
                words = regex.search(line)
                words = words.groups()
                key = words[0]
                elems = words[1].split(',')
                rules[key] = elems
            else:
                words = regex2.search(line)
                words = words.groups()
                words = tuple([int(word) for word in words])
                
                values.append(words)
    
    for value in values:
        result1 += p1(rules, value)
    
    ranges = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
    result2 = p2(rules, 'in', ranges)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

def split_ranges(ranges, idx, num):
    ranges1 = deepcopy(ranges)
    ranges2 = deepcopy(ranges)
    ranges1[idx][1] = num
    ranges2[idx][0] = num + 1
    return ranges1, ranges2

def p2(rules, key, ranges):
    if key == 'A':
        prod = 1
        prod *= (ranges[0][1] - ranges[0][0] + 1)
        prod *= (ranges[1][1] - ranges[1][0] + 1)
        prod *= (ranges[2][1] - ranges[2][0] + 1)
        prod *= (ranges[3][1] - ranges[3][0] + 1)
        return prod
    if key == 'R':
        return 0
    res = 0
    ops = rules[key]
    for op in ops[0:-1]:
        left, right = op.split(':')
        idx = to_idx[left[0]]
        comp = left[1]
        num = int(left[2:])
        if comp == '<':
            if num < ranges[idx][0]:
                continue
            elif num > ranges[idx][1]:
                new_ranges = deepcopy(ranges)
                ranges = None
            else:
                new_ranges, ranges = split_ranges(ranges, idx, num-1)
            res += p2(rules, right, new_ranges)
        elif comp == '>':
            if num > ranges[idx][1]:
                continue
            elif num < ranges[idx][0]:
                new_ranges = deepcopy(ranges)
                ranges = None
            else:
                ranges, new_ranges = split_ranges(ranges, idx, num)
            res += p2(rules, right, new_ranges)
        if ranges is None:
            break
    if ranges is None:
        return res
    if ops[-1] == 'A':
        res += p2(rules, 'A', ranges)
    elif ops[-1] == 'R':
        pass
    else:
        res += p2(rules, ops[-1], ranges)
    return res

def p1(rules, value):
    res = 0
    ops = rules['in']
    while True:
        new_key = None
        for op in ops[0:-1]:
            left, right = op.split(':')
            idx = to_idx[left[0]]
            comp = left[1]
            num = int(left[2:])
            if comp == '<' and value[idx] < num:
                new_key = right
                break
            elif comp == '>' and value[idx] > num:
                new_key = right
                break
        if new_key is not None and new_key not in 'AR':
            ops = rules[new_key]
            continue
        elif new_key == 'A':
            res += sum(value)
            break
        elif new_key == 'R':
            break
        if ops[-1] == 'A':
            res += sum(value)
            break
        elif ops[-1] == 'R':
            break
        else:
            ops = rules[ops[-1]]
    return res

run(lines_test)
run(lines)