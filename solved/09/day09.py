#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 9
def get_year(): return 2022

def sig(x):
    if x == 0: return 0
    if x < 0: return -1
    return 1

def mv(T, H):
    (tx, ty), (hx, hy) = T, H
    dx, dy = hx - tx, hy - ty
    if abs(dx) > 1 or abs(dy) > 1:
        ddx, ddy = sig(dx), sig(dy)
        tx, ty = tx + ddx, ty + ddy
    return tx, ty

def pGrid(snake):
    def toG(x, y):
        return 6-y, 6+x
    coords = [toG(x, y) for x, y in snake]
    G = [list('.'*13) for _ in range(13)]

    for i, (x, y) in enumerate(snake):
        r, c = toG(x, y)
        if G[r][c] == '.':
            G[r][c] = str(i)
    print('\n'.join(''.join(l) for l in G))

def getTailTrail(inp, L):
    lns = get_lines(inp)
    snake = [(0,0) for _ in range(L)]
    tails = set()
    tails.add((0, 0))
    DIR = {
        'U' : (0, 1),
        'L' : (-1, 0),
        'R' : (1, 0),
        'D' : (0, -1)
    }
    for ln in lns:
        d, n = lazy_ints(ln.split())
        dx, dy = DIR[d]
        for _ in range(n):
            snake[0] = snake[0][0] + dx, snake[0][1] + dy
            for i in range(1, len(snake)):
                snake[i] = mv(snake[i], snake[i-1])
            tails.add(snake[-1])

    return len(tails)


def p1(v):
    return getTailTrail(v, 2)

def p2(v):
    return getTailTrail(v, 10)


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
