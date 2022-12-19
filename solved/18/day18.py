#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 18
def get_year(): return 2022

def neighbours(x,y,z):
    return [
        (x-1,y,z),
        (x+1,y,z),
        (x,y-1,z),
        (x,y+1,z),
        (x,y,z-1),
        (x,y,z+1),
    ]

def inside(T, box):
    for c, (min_c, max_c) in zip(T, box):
        if not (min_c <= c <= max_c): return False
    return True


def p1(v):
    lns = get_lines(v)
    cells = [tuple(int(x) for x in ln.split(',')) for ln in lns]
    ans = 0
    cubes = set(cells)

    ans = 0
    for x, y, z in cells:
        for T in neighbours(x,y,z):
            if T not in cubes:
                ans += 1
    return ans

# not 2712, 1116
def p2(v):
    lns = get_lines(v)
    cells = [tuple(int(x) for x in ln.split(',')) for ln in lns]
    ans = 0
    cubes = set(cells)

    C = Counter()
    for x, y, z in cells:
        for T in neighbours(x,y,z):
            if T not in cubes:
                C[T] += 1

    box = []
    for i in range(3):
        mn = min(cubes, key=lambda c: c[i])[i] - 2
        mx = max(cubes, key=lambda c: c[i])[i] + 2
        box.append((mn, mx))

    q = [(box[0][0], box[1][0], box[2][0])]
    vis = set(q)
    ans = 0
    while q:
        q2 = []
        for x, y, z in q:
            for T in neighbours(x, y, z):
                if T not in vis and T not in cubes and inside(T, box):
                    q2.append(T)
                    vis.add(T)
                if T in cubes:
                    ans += 1
        q = q2
    return ans


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
