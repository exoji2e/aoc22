#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 4
def get_year(): return 2022

def parse(line):
    a1, a2, b1, b2 = lazy_ints(multi_split(line, '-,'))
    return a1, a2, b1, b2
def overlaps(line):
    a1, a2, b1, b2 = parse(line)
    if a1 <= b1 <= a2: return True
    if a1 <= b2 <= a2: return True
    return False
def contains(line):
    a1, a2, b1, b2 = parse(line)
    if a1 <= b1 <= b2 <= a2: return True
    if b1 <= a1 <= a2 <= b2: return True
    return False


def p1(v):
    lns = get_lines(v)
    return sum(contains(ln) for ln in lns)

def p2(v):
    lns = get_lines(v)
    return sum(overlaps(ln) for ln in lns)


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
