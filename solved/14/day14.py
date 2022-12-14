#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 14
def get_year(): return 2022

def getRocks(v):
    lns = get_lines(v)
    rocks = set()
    for ln in lns:
        arr = ln.split('->')
        for i in range(len(arr) - 1):
            x0, y0 = map(int, arr[i].split(','))
            x1, y1 = map(int, arr[i+1].split(','))
            for x in range(min(x0, x1), max(x0, x1)+1):
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    rocks.add((x, y))
    return rocks

def fall(blocked, limit):
    x, y = 500, 0
    while True:
        if y > limit:
            break
        if (x, y+1) not in blocked:
            y += 1
            continue
        if (x-1, y+1) not in blocked:
            x -= 1
            y += 1
            continue
        if (x+1, y+1) not in blocked:
            x, y = x+1, y+1
            continue
        break
    return y < limit, x, y

def p1(v):
    rocks = getRocks(v)
    maxY = max(y for _, y in rocks) + 2
    blocked = rocks
    cnt = 0
    while True:
        ok, x, y = fall(blocked, maxY)
        if ok:
            cnt += 1
            blocked.add((x, y))
        else:
            break
    return cnt

def p2(v):
    rocks = getRocks(v)
    maxY = max(y for _, y in rocks) + 2
    for x in range(-5000, 5000):
        rocks.add((x, maxY))
    blocked = rocks
    cnt = 0
    while (500, 0) not in blocked:
        ok, x, y = fall(blocked, maxY)
        if ok:
            cnt += 1
            blocked.add((x, y))
        else:
            break
    return cnt


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
