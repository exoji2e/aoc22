#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 23
def get_year(): return 2022

def test(r, c, pos, d):
    if d == 0:
        if all((x, y) not in pos for x, y in [(r-1, c-1), (r-1, c), (r-1, c+1)]):
            return True, (r-1, c)
    if d == 1:
        if all((x, y) not in pos for x, y in [(r+1, c-1), (r+1, c), (r+1, c+1)]):
            return True, (r+1, c)
    if d == 2:
        if all((x, y) not in pos for x, y in [(r-1, c-1), (r, c-1), (r+1, c-1)]):
            return True, (r, c-1)
    if d == 3:
        if all((x, y) not in pos for x, y in [(r-1, c+1), (r, c+1), (r+1, c+1)]):
            return True, (r, c+1)
    return False, None


def round(pos, i):
    prop = defaultdict(list)
    for r, c in pos:
        ok = True
        for rr, cc in grid8n(r,c):
            if (rr, cc) in pos: ok = False
        if ok:
            prop[r,c].append((r, c))
            continue
        for d in range(4):
            ok, crd = test(r,c, pos, (i + d)%4)
            if ok:
                prop[crd].append((r,c))
                break
        if not ok:
            prop[r, c].append((r, c))

    pos2 = set()
    # print(prop)
    moved = False
    for target, L in prop.items():
        if len(L) == 1:
            pos2.add(target)
            moved = moved or (target != L[0])
        else:
            for p in L:
                pos2.add(p)
    return pos2, moved

def parse(v):
    lns = get_lines(v)
    pos = set()
    for r, ln in enumerate(lns):
        for c, ch in enumerate(ln):
            if ch == '#':
                pos.add((r, c))
    return pos

# 998
def p1(v):
    pos = parse(v)
    for i in range(10):
        pos, _ = round(pos, i)

    mnx = min(pos)[0]
    mny = min(pos, key=lambda c: c[1])[1]
    mxx = max(pos)[0]
    mxy = max(pos, key=lambda c: c[1])[1]
    dx = mxx - mnx + 1
    dy = mxy - mny + 1
    return dx*dy - len(pos)

def p2(v):
    pos = parse(v)
    i = 0
    moved = True
    while moved:
        pos, moved = round(pos, i)
        i += 1
    return i


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
