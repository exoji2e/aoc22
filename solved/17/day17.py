#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 17
def get_year(): return 2022


rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    ]

def move(dx, dy, x, y, rock, grid):
    x2, y2 = x + dx, y + dy
    for ddx, ddy in rock:
        if (x2 + ddx, y2 + ddy) in grid:
            return 0, 0
    return dx, dy

def pRockGrid(rock, X, Y, grid, maxh):
    g2 = {(x, y): '#' for x, y in grid if y <= maxh + 2}
    for dx, dy in rock:
        g2[X+ dx, Y + dy] = '@'
    printCoords(g2)

def fall(rock, grid, maxh, actions, i):
    x, y = 3, maxh + 4
    while True:
        dx, dy = move(getAction(actions), 0, x, y, rock, grid)
        x, y = x + dx, y + dy

        dx, dy = move(0, -1, x, y, rock, grid)
        if dy == 0:
            break
        x, y = x + dx, y + dy

    for dx, dy in rock:
        grid.add((x+dx, y+dy))
        maxh = max(maxh, y + dy)
    return maxh

def getAction(actions):
    global actionsUsed
    a = actions[actionsUsed%len(actions)]
    actionsUsed += 1
    return a

def p1(v):
    v = v.strip()
    global actionsUsed
    actionsUsed = 0
    actions = [-1 if ch == '<' else 1 for ch in v]
    grid = set()
    for i in range(9):
        grid.add((i, 0))
    for i in range(10**6):
        grid.add((0, i))
        grid.add((8, i))
    maxh = 0
    for i in range(2022):
        rock = rocks[i%len(rocks)]
        maxh = fall(rock, grid, maxh, actions, i)
        i += 1
    return maxh

def p2(v):
    v = v.strip()
    global actionsUsed
    actionsUsed = 0
    actions = [-1 if ch == '<' else 1 for ch in v]
    grid = set()
    for i in range(9):
        grid.add((i, 0))
    for i in range(10**6):
        grid.add((0, i))
        grid.add((8, i))
    maxh = 0
    states = {}
    skipFirst = 1000
    hs = []
    i = 0
    while True:
        state = i%len(rocks), actionsUsed%len(actions)
        if state in states:
            skipFirst -= 1
            if skipFirst < 0:
                (c, h), (lc, lh) = (i, maxh), states[state]
                dc = c - lc
                dh = h - lh
                break
        states[state] = i, maxh
        hs.append(maxh)
        rock = rocks[i%len(rocks)]
        maxh = fall(rock, grid, maxh, actions, i)
        i += 1
    (c, h), (lc, lh) = (i, maxh), states[state]
    dc = c - lc
    dh = h - lh
    L = 1000000000000
    rem = L - c
    laps = rem//dc
    left = rem%dc
    H = h + laps*dh
    C = c + laps*dc
    left2 = L - C
    assert left == left2
    extrah = hs[lc + left] - lh
    return H + extrah


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
