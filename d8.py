from typing import List
import utils
import re
import math

lines_test = utils.parse("d8test.txt")
lines = utils.parse("d8.txt")

line_re = r'(.+) = \((.+)\, (.+)\)'

def build_graph(lines: List[str], graph):
    for line in lines:
        match = re.match(line_re, line)
        groups = match.groups()
        graph[groups[0]] = (groups[1], groups[2])



@utils.measure
def run(lines):
    moves = 0
    sum2 = 0

    instructions = lines[0]
    n_instructions = len(instructions)
    graph = dict()
    build_graph(lines[2:], graph)

    # current_pos = 'AAA'
    # while current_pos != 'ZZZ':
    #     current_pos = graph[current_pos][1] if instructions[moves%n_instructions] == 'R' else graph[current_pos][0]
    #     moves+=1

    current_nodes = []
    for line in lines[2:]:
        if line[2] == 'A':
            current_nodes.append(line.split()[0])
    n_moves = [0 for _ in current_nodes]
    

    for i, node in enumerate(current_nodes):
        while current_nodes[i][2] != 'Z':
            current_nodes[i] = graph[current_nodes[i]][0] if instructions[n_moves[i]%n_instructions] == 'L' else graph[current_nodes[i]][1]
            n_moves[i] += 1

    moves2 = math.lcm(*n_moves)

    print(f'Part 1: {moves}')
    print(f'Part 2: {moves2}')

run(lines_test)
run(lines)