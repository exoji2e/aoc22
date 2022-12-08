#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 8
def get_year(): return 2022

def parse(v):
    lns = get_lines(v)
    return lns

def sceneScore(G, r, c):
    R, C = len(G), len(G[0])
    scs = []
    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        h = G[r][c]
        cnt = 0
        r0, c0 = r +dr, c + dc
        while 0 <= r0 < R and 0 <= c0 < C:
            cnt += 1
            if G[r0][c0] >= h:
                break
            r0, c0 = r0 + dr, c0 + dc
        scs.append(cnt)
    return scs[0]*scs[1]*scs[2]*scs[3]

def p1(v):
    lns = get_lines(v)
    g = [[int(ch) for ch in ln] for ln in lns]
    trees = set()
    R, C = len(g), len(g[0])
    for r in range(R):
        mx = -1
        for c in range(C):
            if g[r][c] > mx:
                trees.add((r, c))
                mx = g[r][c]
        mx = -1
        for c in range(C)[::-1]:
            if g[r][c] > mx:
                trees.add((r, c))
                mx = g[r][c]
    for c in range(C):
        mx = -1
        for r in range(R):
            if g[r][c] > mx:
                trees.add((r, c))
                mx = g[r][c]
        mx = -1
        for r in range(R)[::-1]:
            if g[r][c] > mx:
                trees.add((r, c))
                mx = g[r][c]
    return len(trees)

def p2(v):
    lns = get_lines(v)
    g = [[int(ch) for ch in ln] for ln in lns]
    trees = set()
    R, C = len(g), len(g[0])
    mxScore = 0, (0, 0)
    for r in range(R):
        for c in range(C):
            mxScore = max(mxScore, (sceneScore(g, r, c), (r, c)))
    return mxScore[0]


if __name__ == '__main__':
    cmds = get_commands()
    """
    cmds = [
        #'print_stats',
        'run1',
        #'submit1',
        #'run2',
        #'submit2',
        ]
    """
    print('Commands:', cmds)
    main(get_year(), get_day(), p1, p2, cmds, FILE=__file__)
