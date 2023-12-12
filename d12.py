from typing import List, Tuple
import utils
import functools

lines_test = utils.parse("d12test.txt")
lines = utils.parse("d12.txt")

@functools.cache
def count_possibilities(pattern: str, numbers: str, char_pos: int, seq_pos: int, num_pos: int) -> int:
    if char_pos == len(pattern):
        if num_pos == len(numbers) and seq_pos == 0:
            result = 1
        elif num_pos == len(numbers) - 1:
            if seq_pos == numbers[num_pos]:
                result = 1
            else:
                result = 0
        else:
            result = 0
    elif pattern[char_pos] == '#':
        result = count_possibilities(pattern, numbers, char_pos + 1, seq_pos + 1, num_pos)
    elif pattern[char_pos] == '.' or num_pos == len(numbers):
        if num_pos < len(numbers) and seq_pos == numbers[num_pos]:
            result = count_possibilities(pattern, numbers, char_pos + 1, 0, num_pos + 1)
        elif seq_pos == 0:
            result = count_possibilities(pattern, numbers, char_pos + 1, 0, num_pos)
        else:
            result = 0
    else:
        hash_result = count_possibilities(pattern, numbers, char_pos + 1, seq_pos + 1, num_pos)
        dot_result = 0
        if seq_pos == numbers[num_pos]:
            dot_result = count_possibilities(pattern, numbers, char_pos + 1, 0, num_pos + 1)
        elif seq_pos == 0:
            dot_result = count_possibilities(pattern, numbers, char_pos + 1, 0, num_pos)
        result = hash_result + dot_result
    return result

@utils.measure
def run(lines: List[str]):
    
    result1 = 0
    result2 = 0

    for line in lines:
        pattern, numbers = line.split()
        numbers = numbers.split(',')
        numbers = [int(number) for number in numbers]
        numbers = tuple(numbers)
        count = count_possibilities(pattern, numbers, 0, 0, 0)
        result1 += count

    for line in lines:
        pattern, numbers = line.split()
        numbers = numbers.split(',')
        pattern = (pattern + '?') * 4 + pattern
        numbers = [int(number) for number in numbers]
        numbers = numbers * 5
        numbers = tuple(numbers)
        result2 += count_possibilities(pattern, numbers, 0, 0, 0)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run(lines_test)
run(lines)