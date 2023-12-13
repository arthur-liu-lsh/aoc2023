from typing import List, Tuple

import numpy as np
import utils
import functools

lines_test = utils.parse("d13test.txt")
lines = utils.parse("d13.txt")

def find_h_axis(lines):
    axis = []
    for k in range(len(lines)):
        n_lines = min(len(lines) - k - 1, k+1)
        if np.array_equal(lines[k-n_lines+1:k+1], lines[k+n_lines:k:-1]):
            if (lines[k-n_lines+1:k+1].size == 0):
                continue
            axis.append(k)
    return axis

def find_v_axis(lines):
    axis = []
    for k in range(lines.shape[1]):
        n_lines = min(lines.shape[1] - k - 1, k+1)
        if np.array_equal(lines[:,k-n_lines+1:k+1], lines[:,k+n_lines:k:-1]):
            if (lines[:,k-n_lines+1:k+1].size == 0):
                continue
            axis.append(k)
    return axis

@utils.measure
def run(lines: List[str]):
    
    result1 = 0
    result2 = 0

    patterns = [[]]

    for line in lines:
        if line == '':
            patterns.append([])
        else:
            patterns[-1].append(line)
    
    for i in range(len(patterns)):
        pattern = patterns[i]
        pattern = np.array([list(elem) for elem in pattern])
        patterns[i] = np.array(pattern)

    for idx, pattern in enumerate(patterns):
        values1 = find_h_axis(pattern)
        values2 = find_v_axis(pattern)
        value1 = -1
        value2 = -1
        value = 0
        if values1 != []: 
            value1 = 100*(values1[0]+1)
        elif values2 != []:
            value2 = values2[0]+1
        if value1 != -1:
            value = value1
        elif value2 != -1:
            value = value2
        result1 += value
        stop = False
        for i in range(pattern.shape[0]):
            for j in range(pattern.shape[1]):
                new_pattern = pattern.copy()
                if new_pattern[i,j] == '#':
                    new_pattern[i,j] = '.'
                elif new_pattern[i,j] == '.':
                    new_pattern[i,j] = '#'
                new_values1 = find_h_axis(new_pattern)
                new_values2 = find_v_axis(new_pattern)

                new_value1 = -1
                new_value2 = -1
                new_value = 0
                for elem in new_values1:
                    if 100*(elem+1) != value1:
                        new_value1 = 100*(elem+1)
                for elem in new_values2:
                    if elem+1 != value2:
                        new_value2 = elem+1
                if new_value1 != -1 and new_value1 != value1:
                    new_value = new_value1
                elif new_value2 != -1 and new_value2 != value2:
                    new_value = new_value2
                if new_value != 0 and new_value != value:
                    result2 += new_value
                    stop = True
                    break
            if stop:
                break

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')


run(lines_test)
run(lines)