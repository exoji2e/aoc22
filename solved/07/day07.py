#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 7
def get_year(): return 2022

def getDirs(lns, i=0):
    chs = []
    curr = 0
    while i < len(lns):
        ln = lns[i]
        arr = lazy_ints(ln.split())
        if type(arr[0]) == int:
            curr += arr[0]
        elif ln.startswith('$ cd ..'):
            chs.append(curr)
            return chs, curr, i
        elif ln.startswith('$ cd'):
            new_chs, me, i = getDirs(lns, i+1)
            curr += me
            chs.extend(new_chs)
        else: pass
        i += 1
    chs.append(curr)
    return chs, curr, i

def p1(v):
    dirs, _, _ = getDirs(get_lines(v))
    su = sum(k for k in dirs if k <= 100000)
    return su

def p2(v):
    dirs, top, _ = getDirs(get_lines(v))
    FULL = 70000000
    NEED = 30000000
    DEL = NEED - (FULL - top)
    mn = min(k for k in dirs if k >= DEL)
    return mn


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
