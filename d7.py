import utils
import re
from collections import Counter
from functools import cmp_to_key

lines_test = utils.parse("d7test.txt")
lines = utils.parse("d7.txt")

order1 = 'AKQJT98765432'
order2 = 'AKQT98765432J'
types = [[1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 2, 2], [1, 1, 3], [2, 3], [1, 4], [5]]

def compare(line1: str, line2: str):
    elem1 = line1.split()[0]
    elem2 = line2.split()[0]
    
    counter1 = Counter(elem1)
    counter2 = Counter(elem2)

    rank1 = types.index(sorted(counter1.values()))
    rank2 = types.index(sorted(counter2.values()))

    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return -1

    for i in range(len(elem1)):
        index1 = order1.find(elem1[i])
        index2 = order1.find(elem2[i])
        if index1 > index2:
            return -1
        elif index2 > index1:
            return 1
    return 0

def compare2(line1: str, line2: str):
    elem1 = line1.split()[0]
    elem2 = line2.split()[0]
    
    counter1 = Counter(elem1)
    counter2 = Counter(elem2)

    rank1 = types.index(sorted(counter1.values()))
    rank2 = types.index(sorted(counter2.values()))

    if 'J' in elem1:
        rank1 = max([types.index(sorted(Counter(elem1.replace('J', letter)).values())) for letter in order2])
    if 'J' in elem2:
        rank2 = max([types.index(sorted(Counter(elem2.replace('J', letter)).values())) for letter in order2])

    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return -1

    for i in range(len(elem1)):
        index1 = order2.find(elem1[i])
        index2 = order2.find(elem2[i])
        if index1 > index2:
            return -1
        elif index2 > index1:
            return 1
    return 0

@utils.measure
def run(lines):
    sum1 = 0
    sum2 = 0

    sorted_lines = sorted(lines, key=cmp_to_key(compare))
    for i, line in enumerate(sorted_lines):
        words = line.split()
        sum1 += int(words[1]) * (i+1)

    sorted_lines = sorted(lines, key=cmp_to_key(compare2))
    for i, line in enumerate(sorted_lines):
        words = line.split()
        sum2 += int(words[1]) * (i+1)


    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')

run(lines_test)
run(lines)