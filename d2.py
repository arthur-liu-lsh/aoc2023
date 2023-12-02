import utils


lines = utils.parse("d2.txt")


@utils.measure
def run():
    counters = []

    for line in lines:
        words = line.split()
        for i in range(len(words)):
            words[i] = words[i].strip(':,;')
        counter = {}
        n = (len(words)) // 2
        counter['red'] = 0
        counter['green'] = 0
        counter['blue'] = 0
        for j in range(1, n):
            counter[words[j * 2 + 1]] = max(int(words[j * 2]), counter[words[j * 2 + 1]])
        counters.append(counter)

    sum = 0
    power = 0

    for i, counter in enumerate(counters):
        if counter['red'] <= 12 and counter['green'] <= 13 and counter['blue'] <= 14:
            sum += (i+1)
        power += (counter['red'] * counter['green'] * counter['blue'])
    
    print(f'Part 1: {sum}')
    print(f'Part 2: {power}')


run()