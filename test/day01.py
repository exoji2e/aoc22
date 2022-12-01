#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import run, run_samples, get_commands
from utils import *
def get_day(): return 1
def get_year(): return 2021

def p1(v):
    lines = get_lines(v)
    ans = 0
    lst = lazy_ints(lines)
    for i in range(1, len(lst)):
        if lst[i-1] < lst[i]:
            ans += 1

    return ans

def p2(v):
    lines = get_lines(v)
    ans = 0
    last = 10**18
    lst = lazy_ints(lines)
    for i in range(3, len(lst)):
        if sum(lst[i-3:i]) < sum(lst[i-2:i+1]):
            ans += 1

    return ans


if __name__ == '__main__':
    """
    cmds = [
        'run1', 'run2',
        #'print_stats',
        #'submit1',
        #'submit2']
    """
    cmds = get_commands()
    print('Commands:', cmds)
    if 'run_samples' in cmds or 'samples_only' in cmds:
        run_samples(p1, p2, cmds, __file__)
    if 'samples_only' not in cmds:
        run(get_year(), get_day(), p1, p2, cmds, FILE=__file__)
