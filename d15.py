from typing import Dict, List, Set, Tuple

import utils
import functools

lines_test = utils.parse("d15test.txt")
lines = utils.parse("d15.txt")

def get_hash(word: str) -> int:
    value = 0
    for char in word:
        asc = ord(char)
        value += asc
        value *= 17
        value = value % 256
    return value

@utils.measure
def run(lines: List[str]):
    
    result1 = 0
    result2 = 0
    
    line = lines[0]
    words = line.split(',')

    for word in words:
        count = 0
        for char in word:
            asc = ord(char)
            count += asc
            count *= 17
            count = count % 256
        result1 += count

    boxes: Dict[int, Dict[str, int]] = {}

    for word in words:
        elems = word.split('=')
        if len(elems) == 2:
            lens = elems[0]
            lens = int(elems[1])
            box_id = get_hash(lens)
            if box_id not in boxes:
                boxes[box_id] = {}
            boxes[box_id][lens] = lens
        else:
            lens = elems[0][:-1]
            box_id = get_hash(lens)
            if box_id in boxes:
                if lens in boxes[box_id]:
                    boxes[box_id].pop(lens)

    for box_id in boxes:
        for order, lens in enumerate(boxes[box_id].values()):
            result2 += (box_id + 1) * (order + 1) * lens

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')


run(lines_test)
run(lines)