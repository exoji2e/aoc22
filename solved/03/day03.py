#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 3
def get_year(): return 2022

def getSc(s):
    N = len(s)
    a, b = s[:N//2], s[N//2:]
    su = 0
    for i in range(26):
        ch = chr(ord('a') + i)
        if ch in a and ch in b:
            su += i+1
        ch = chr(ord('A') + i)
        if ch in a and ch in b:
            su += i+27
    return su
def getV(c):
    if c == c.lower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

def p1(v):
    lns = get_lines(v)
    ans = sum(getSc(ln) for ln in lns)
    return ans

def p2(v):
    lns = get_lines(v)
    ans = 0
    for i in range(0, len(lns), 3):
        S = set(lns[i]) & set(lns[i+1]) & set(lns[i+2])
        x = S.pop()
        ans += getV(x)

    return ans


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
