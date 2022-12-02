#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import run, run_samples, get_commands
from utils import *
def get_day(): return 1
def get_year(): return 2022

def calc(v):
    chunks = get_chunks(v)
    cals = []
    for ch in chunks:
        ans = 0
        for cal in lazy_ints(ch):
            ans += cal
        cals.append(ans)
    cals.sort()
    return cals

def p1(v):
    return max(calc(v))

def p2(v):
    return sum(calc(v)[-3:])


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
