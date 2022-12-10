#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 10
def get_year(): return 2022


def p1(v):
    lns = get_lines(v)
    X = 1
    sigStr = 0
    cId = 0
    for ln in lns:
        arr = lazy_ints(ln.split())
        for _ in range(len(arr)):
            cId += 1
            if (cId)%40 == 20:
                sigStr += X*(cId)
        if len(arr) == 2:
            X += arr[1]

    return sigStr

def p2(v):
    lns = get_lines(v)
    X = 1
    cId = 0
    G = [list(' '*40) for _ in range(6)]
    for ln in lns:
        arr = lazy_ints(ln.split())
        for _ in range(len(arr)):
            yp, xp = cId//40, cId%40
            if xp-1 <= X <= xp+1:
                G[yp][xp] = '#'
            cId += 1
        if len(arr) == 2:
            X += arr[1]

    return '\n' + '\n'.join(''.join(l) for l in G)


if __name__ == '__main__':
    if '-m' in sys.argv:
        data = sys.stdin.read()
        print(p1(data))
        exit(0)
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
