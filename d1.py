import utils
import re

lines = utils.parse("d1.txt")

convert = {'one':'1',
           'two':'2',
           'three':'3',
           'four':'4',
           'five':'5',
           'six':'6',
           'seven':'7',
           'eight':'8',
           'nine':'9',
           '1':'1',
           '2':'2',
           '3':'3',
           '4':'4',
           '5':'5',
           '6':'6',
           '7':'7',
           '8':'8',
           '9':'9'
           }

@utils.measure
def run():
    sum1 = 0
    sum2 = 0
    for _, line in enumerate(lines):
        numbersStart1 = re.findall(r'(\d).*', line)
        numbersEnd1 = re.findall(r'.*(\d)', line)
        numbersStart2 = re.findall(r'(one|two|three|four|five|six|seven|eight|nine|\d).*', line)
        numbersEnd2 = re.findall(r'.*(one|two|three|four|five|six|seven|eight|nine|\d)', line)
        combined1 = convert[numbersStart1[0]] + convert[numbersEnd1[-1]]
        combined2 = convert[numbersStart2[0]] + convert[numbersEnd2[-1]]
        sum1 += int(combined1)
        sum2 += int(combined2)
    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')

run()