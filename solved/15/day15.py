#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 15
def get_year(): return 2022

def parse(v):
    sensors = []
    Y_TARG, HI = 2000000, 4000000
    for ln in get_lines(v):
        ln = ln.replace(',', ' ').replace('=', ' ').replace(':', ' ')
        arr = [x for x in lazy_ints(ln.split()) if type(x) == int]
        if len(arr) == 2:
            Y_TARG, HI = arr
        else:
            sensors.append(arr)
    return sensors, Y_TARG, HI

# 5587312
def p1(v):
    sensors, Y_TARGET, _ = parse(v)
    Is = []
    Bs = set()
    for sx, sy, bx, by in sensors:
        if by == Y_TARGET:
            Bs.add(bx)
        if sy == Y_TARGET:
            Is.append((sx, sx))
        md = abs(sx-bx) + abs(sy-by)
        delta = md - abs(sy - Y_TARGET)
        if delta >= 0:
            Is.append((sx - delta, sx + delta))

    S = set()
    for a, b in Is:
        S |= set(range(a, b+1))
    return len(S) - len(Bs)

def p2(v):
    sensors, _, HI = parse(v)
    Is = [[] for _ in range(HI + 1)]
    for sx, sy, bx, by in sensors:
        if 0 <= by <= HI:
            Is[by].append((bx, bx))
        if 0 <= sy <= HI:
            Is[sy].append((sx, sx))
        md = abs(sx-bx) + abs(sy-by)
        for y in range(max(sy - md, 0), min(sy + md, HI) + 1):
            if y > HI: break
            delta = md - abs(sy - y)
            Is[y].append((sx - delta, sx + delta))

    for y in range(HI+1):
        if y%1000000 == 0:
            print(f'Y coord: {y} / {HI}')
        Is[y].sort()
        CM = -1
        for a, b in Is[y]:
            if a > CM + 1:
                x = CM + 1
                print(x, y)
                return x*4000000 + y
            CM = max(CM, b)


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
