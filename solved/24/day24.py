#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 24
def get_year(): return 2022

DF = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}

def parse(v):
    lns = get_lines(v)
    bzd = []
    for r, ln in enumerate(lns):
        for c, ch in enumerate(ln):
            if ch in '<>v^':
                bzd.append((r, c, ch))

    R, C = len(lns), len(lns[0])
    return lns, bzd, R, C

def create_walk_fn(lns, bzd, R, C):

    bzdOnTime = {}
    def getBzdSet(t):
        if t in bzdOnTime: return bzdOnTime[t]
        S = set()
        for r0, c0, d in bzd:
            dr, dc = DF[d]
            cr, cc = (r0 + t*dr - 1)%(R-2) + 1, (c0 + t*dc - 1)%(C-2) + 1
            S.add((cr, cc))
        bzdOnTime[t] = S
        return S

    def has_bzd(r, c, t):
        return (r, c) in getBzdSet(t)

    def walk(SRC, DST, time):
        r,c = SRC
        q = [(r, c, time)]
        vis = set(q)
        while q:
            q2 = []
            for r, c, t in q:
                if r == DST[0]: return t
                for rr, cc in grid4nf(r, c, R, C) + [(r, c)]:
                    if lns[rr][cc] == '#': continue
                    T = rr, cc, t+1
                    if T in vis: continue
                    if has_bzd(rr, cc, t+1): continue
                    q2.append(T)
                    vis.add(T)
            q = q2
    return walk


def p1(v):
    lns, bzd, R, C = parse(v)
    walk = create_walk_fn(lns, bzd, R, C)
    return walk((0, 1), (R-1, C-2), 0)


def p2(v):
    lns, bzd, R, C = parse(v)
    walk = create_walk_fn(lns, bzd, R, C)
    S = (0, 1)
    T = (R-1, C-2)
    t = walk(S, T, 0)
    t = walk(T, S, t)
    t = walk(S, T, t)
    return t


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
