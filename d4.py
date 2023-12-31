import utils
import re

lines = utils.parse("d4.txt")

@utils.measure
def run():
    sum1 = 0
    sum2 = 0

    counter = [1 for _ in lines]
    for i, line in enumerate(lines):
        words = line.split()
        sep_index = words.index('|')
        winning_numbers = words[2:sep_index]
        playing_numbers = words[sep_index+1:]
        count1 = 0
        count2 = 0
        for elem in playing_numbers:
            if elem in winning_numbers:
                if count1 == 0:
                    count1 = 1
                else:
                    count1 *=2
                count2 += 1
        for k in range(count2):
            counter[i+k+1] += 1 * counter[i]
        sum1 += count1
    sum2 = sum(counter)


    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')

run()