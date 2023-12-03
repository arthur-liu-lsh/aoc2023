import utils



lines = utils.parse("d3.txt")

def neighbours(array, i, j, n, m):
    adj = []
    if (i < n-1) and j > 0:
        adj.append(array[i+1][j-1])
    if (i < n-1):
        adj.append(array[i+1][j])
    if (i < n-1) and (j < m-1):
        adj.append(array[i+1][j+1])
    if (i > 0):
        adj.append(array[i-1][j])
    if (i > 0) and (j > 0):
        adj.append(array[i-1][j-1])
    if (i > 0) and (j < m):
        adj.append(array[i-1][j+1])
    if (j < m-1):
        adj.append(array[i][j+1])
    if (j > 0):
        adj.append(array[i][j-1])
    return adj

def coord_neighbours(array, i, j, n, m):
    adj = []
    if (i < n-1) and j > 0:
        adj.append((i+1,j-1))
    if (i < n-1):
        adj.append((i+1,j))
    if (i < n-1) and (j < m-1):
        adj.append((i+1,j+1))
    if (i > 0):
        adj.append((i-1,j))
    if (i > 0) and (j > 0):
        adj.append((i-1,j-1))
    if (i > 0) and (j < m):
        adj.append((i-1, j+1))
    if (j < m-1):
        adj.append((i,j+1))
    if (j > 0):
        adj.append((i,j-1))
    return adj

@utils.measure
def run():
    sum1 = 0

    n = len(lines)
    m = len(lines[0])
    for i, line in enumerate(lines):
        current_number = ''
        for j, char in enumerate(line):
            if char in "1234567890":
                current_number += char
            else:
                # sum += currentNumber
                if current_number != '':
                    isValid = False
                    
                    for k, current_letter in enumerate(current_number):
                        adj = neighbours(lines, i, j-len(current_number)+k, n, m)
                        filtered = [elem for elem in adj if elem not in '1234567890.']
                        if len(filtered) != 0:
                            isValid = True
                    if isValid:
                        sum1 += int(current_number)
                    current_number = ''

        if current_number != '':
            isValid = False
        
            for k, current_letter in enumerate(current_number):
                adj = neighbours(lines, i, j-len(current_number)+k, n, m)
                filtered = [elem for elem in adj if elem not in '1234567890.']
                if len(filtered) != 0:
                    isValid = True
            if isValid:
                    sum1 += int(current_number)
            current_number = ''

    numbers = []
    for i in range(n):
        current_number = ''
        current_coords = set()
        for j in range(m):
            char = lines[i][j]
            if char in "1234567890":
                current_number += char
                current_coords.add((i,j))
            else:
                if current_number != '':
                    numbers.append((int(current_number), current_coords))
                    current_number = ''
                    current_coords = set()
        if current_number != '':
            numbers.append((int(current_number), current_coords))
            current_number = ''
            current_coords = set()
    
    sum2 = 0


    for i in range(n):
        for j in range(m):
            char = lines[i][j]
            if char == '*':
                current_neighbours = []
                for coord in coord_neighbours(lines, i, j, n, m):
                    for number in numbers:
                        if coord in number[1]:
                            if number not in current_neighbours:
                                current_neighbours.append(number)
                if len(current_neighbours) == 2:
                    sum2 += current_neighbours[0][0] * current_neighbours[1][0]


    print(f'Part 1: {sum1}')
    print(f'Part 2: {sum2}')


run()