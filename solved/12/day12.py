#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
import utils
def get_day(): return 12
def get_year(): return 2022

def find(ch, G):
    for r in range(len(G)):
        for c in range(len(G[0])):
            if G[r][c] == ch: return r, c

def parse(v):
    lns = get_lines(v)
    G = [list(ln) for ln in lns]
    S = find('S', G)
    E = find('E', G)
    G[S[0]][S[1]] = 'a'
    G[E[0]][E[1]] = 'z'
    return G, S, E

def bfs(S, E, G):
    q = [S]
    V = set(q)
    s = -1
    R, C = len(G), len(G[0])
    while q:
        s += 1
        q2 = []
        for r, c in q:
            if (r, c) == E:
                return s
            h = G[r][c]
            for rr, cc in grid4nf(r, c, R, C):
                if (rr, cc) in V: continue
                if G[rr][cc] <= chr(ord(h) + 1):
                    V.add((rr, cc))
                    q2.append((rr, cc))
        q = q2
    return 10**18


def p1(v):
    G, S, E = parse(v)
    return bfs(S, E, G)

def p2(v):
    G, S, E = parse(v)
    best = 10**18
    for i in range(len(G)):
        for j in range(len(G[0])):
            if G[i][j] == 'a':
                best = min(best, bfs((i, j), E, G))
    return best


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
