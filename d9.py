from typing import List
import utils
import numpy as np

lines_test = utils.parse("d9test.txt")
lines = utils.parse("d9.txt")



@utils.measure
def run(lines: List[str]):
    sum1 = 0
    sum2 = 0

    for i, line in enumerate(lines):
        words = line.split()
        words = [int(word) for word in words]

        temp = np.array(words, dtype=np.int64)
        initials = []
        finals = []
        while any(temp != 0):
            initials.append(temp[0])
            finals.append(temp[-1])
            temp = temp[1:] - temp[0:temp.size-1]
        order = len(initials)


        value_final = finals[-1]
        value_initial = initials[-1]
        for k in range(order - 1):
            value_final = finals[-2-k] + value_final
            value_initial = initials[-2-k] - value_initial
        sum1 += value_final
        sum2 += value_initial

    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')

run(lines_test)
run(lines)