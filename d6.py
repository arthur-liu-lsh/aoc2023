from typing import List, Tuple
import utils
import math

lines = utils.parse("d6.txt")

@utils.measure
def run():
    times = [int(elem) for elem in (lines[0].split()[1:])]
    distances = [int(elem) for elem in (lines[1].split()[1:])]

    n = len(times)
    counts = []

    for i in range(n):
        time = times[i]
        distance = distances[i]
        delta = math.sqrt(time**2-4*distance)
        value = math.ceil((time + delta)/2) - math.floor((time - delta)/2) - 1
        counts.append(value)

    print(counts)

    result1 = 1
    for elem in counts:
        result1 *= elem

    time2 = int("".join(lines[0].split()[1:]))
    distance2 = int("".join(lines[1].split()[1:]))
    delta = math.sqrt(time2**2-4*distance2)
    result2 = math.ceil((time2 + delta)/2) - math.floor((time2 - delta)/2) - 1
    

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run()