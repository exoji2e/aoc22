#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 6
def get_year(): return 2022

def findIndex(v, L):
    for i in range(L, len(v)):
        if len(set(v[i-L:i])) == L:
            return i

def p1(v):
    return findIndex(v, 4)

def p2(v):
    return findIndex(v, 14)


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
