#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 22
def get_year(): return 2022

def parse(v):
    chunks = v.split('\n\n')
    G = chunks[0].split('\n')
    mv = chunks[1]
    mv = mv.replace('L', ' L ').replace('R', ' R ').split()
    valid = set()
    fc = None
    for r in range(len(G)):
        for c in range(len(G[r])):
            if G[r][c] == ' ': continue
            if r == 0 and fc == None: fc = c
            valid.add((r, c))
    return G, valid, fc, mv

DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def p1(v):
    G, valid, fc, mv = parse(v)
    def wrap(nr, nc, d):
        d2 = (d + 2)%4
        last_ok = nr, nc
        while (nr, nc) in valid:
            last_ok = nr, nc
            nr, nc = nr + DIR[d2][0], nc + DIR[d2][1]
        return last_ok

    r, c, d = 0, fc, 0
    for th in mv:
        if th == 'L':
            d = (d - 1)%4
            continue
        if th == 'R':
            d = (d + 1)%4
            continue
        L = int(th)
        for _ in range(L):
            nr, nc = r + DIR[d][0], c + DIR[d][1]
            if (nr, nc) not in valid:
                nr, nc = wrap(r, c, d)
                assert (nr, nc) in valid
            if G[nr][nc] == '.':
                r, c = nr, nc
    return (r + 1) * 1000 + 4 * (c + 1) + d

# part_1: "28423" - copied to clipboard
    """
    Assumes the grid has the following shape:
     21
     3
    54
    6
    """
def p2(v):
    G, valid, fc, mv = parse(v)

    EDGS = {
        (6, 0) : (4, 3),
        (6, 1) : (1, 1),
        (6, 2) : (2, 1),
        (5, 2) : (2, 0),
        (5, 3) : (3, 0),
        (4, 1) : (6, 2),
        (4, 0) : (1, 2),
        (3, 0) : (1, 3),
        (3, 2) : (5, 1),
        (2, 2) : (5, 0),
        (2, 3) : (6, 0),
        (1, 0) : (4, 2),
        (1, 1) : (3, 2),
        (1, 3) : (6, 3)

    }
    Cell = {
        1: (0, 50, 100, 150),
        2: (0, 50, 50, 100),
        3: (50, 100, 50, 100),
        4: (100, 150, 50, 100),
        5: (100, 150, 0, 50),
        6: (150, 200, 0, 50),
    }
    def rc2Cell(r, c):
        for k, (r0, re, c0, ce) in Cell.items():
            if r0 <= r < re and c0 <= c < ce:
                return k

    def celloffsetEdg(cId, offset, edg):
        r0, re, c0, ce = Cell[cId]
        if edg == 0:
            return r0 + offset, ce - 1
        if edg == 1:
            return re - 1, c0 + offset
        if edg == 2:
            return r0 + offset, c0
        if edg == 3:
            return r0, c0 + offset


    def wrap(nr, nc, d):
        cid = rc2Cell(nr, nc)
        nCId, nd = EDGS[cid, d]
        nedg = (nd - 2)%4
        offset = nr%50 if d % 2 == 0 else nc % 50
        if (d, nedg) in {(2, 2), (0, 0)}:
            offset = 50 - 1 - offset
        nr, nc = celloffsetEdg(nCId, offset, nedg)
        return nr, nc, nd


    def test(a, b):
        wa = wrap(*a)
        if wa != b:
            print(a, '->', wa, '!=', b)
            exit(1)
    test((49, 100, 1), (50, 99, 2))

    r, c, d = 0, fc, 0
    for th in mv:
        if th == 'L':
            d = (d - 1)%4
            continue
        if th == 'R':
            d = (d + 1)%4
            continue
        L = int(th)
        for _ in range(L):
            nr, nc = r + DIR[d][0], c + DIR[d][1]
            if (nr, nc) not in valid:
                nr, nc, d = wrap(r, c, d)
                assert (nr, nc) in valid
            if G[nr][nc] == '.':
                r, c = nr, nc
    return (r + 1) * 1000 + 4 * (c + 1) + d


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
