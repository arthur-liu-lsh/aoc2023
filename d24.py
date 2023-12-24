from collections import deque
from typing import Deque, Dict, List, Set, Tuple
import re

import utils
import functools
import numpy as np
import matplotlib.pyplot as plt
import z3

lines_test = utils.parse("d24test.txt")
lines = utils.parse("d24.txt")

regex = re.compile(r'(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*@\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)')

def move_particle(particle, n_iter = 1):
    x, y, z, dx, dy, dz = particle
    x += dx * n_iter
    y += dy * n_iter
    z += dz * n_iter
    return x, y, z, dx, dy, dz

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def is_past(p1, p2, intersect):
    x1, y1, z1, dx1, dy1, dz1 = p1
    x2, y2, z2, dx2, dy2, dz2 = p2
    sx1 = 1 if dx1 > 0 else -1
    sy1 = 1 if dy1 > 0 else -1
    sx2 = 1 if dx2 > 0 else -1
    sy2 = 1 if dy2 > 0 else -1
    ix, iy = intersect
    if (ix - x1) * sx1 < 0 and (iy - y1) * sy1 < 0:
        return True
    if (ix - x2) * sx2 < 0 and (iy - y2) * sy2 < 0:
        return True
    return False

def solve(particles):
    x = z3.Real('x')
    y = z3.Real('y')
    z = z3.Real('z')
    dx = z3.Real('dx')
    dy = z3.Real('dy')
    dz = z3.Real('dz')
    t = z3.RealVector('t', len(particles))
    s = z3.Solver()
    for k, p in enumerate(particles):
        px, py, pz, pdx, pdy, pdz = p
        s.add(px + pdx * t[k] == x + dx * t[k])
        s.add(py + pdy * t[k] == y + dy * t[k])
        s.add(pz + pdz * t[k] == z + dz * t[k])
    s.check()
    model = s.model()
    res = model.eval(x), model.eval(y), model.eval(z), model.eval(dx), model.eval(dy), model.eval(dz)
    res = tuple([elem.as_long() for elem in res])
    return res

@utils.measure
def run(lines: List[str], boundaries: Tuple[int, int]):

    result1 = 0
    result2 = 0

    particles = []

    for line in lines:
        groups = [int(elem) for elem in regex.match(line).groups()]
        particles.append(groups)

    crossed = [False for _ in particles]

    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i == j:
                continue
            if i > j:
                continue
            if crossed[i] or crossed[j]:
                continue
            x1, y1, z1, _, _, _ = p1
            x2, y2, z2, _, _, _ = move_particle(p1)
            x3, y3, z3, _, _, _ = p2
            x4, y4, z4, _, _, _ = move_particle(p2)
            intersect = line_intersection(((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)))
            if intersect is not None:
                if (boundaries[0] <= intersect[0] <= boundaries[1]) and (boundaries[0] <= intersect[1] <= boundaries[1]):
                    if not is_past(p1, p2, intersect):
                        result1 += 1

    x, y, z, dx, dy, dz = solve(particles)
    result2 = x + y + z

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')

run(lines_test, (7, 27))
run(lines, (200000000000000, 400000000000000))
