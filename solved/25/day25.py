#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 25
def get_year(): return 2022

def convert(s):
    curr = 0
    for ch in s:
        curr *= 5
        curr += Nbrs[ch]
    return curr

Nbrs = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

def snafu(no):
    R = {v: k for k, v in Nbrs.items()}
    out = []
    while no > 0:
        m = no%5
        if m >= 3:
            m -= 5
            no += 5
        out.append(R[m])
        no //= 5
    return ''.join(out[::-1])


def p1(v):
    lns = get_lines(v)
    ans = 0
    for ln in lns:
        ans += convert(ln)
    return snafu(ans)

def p2(v):
    return 'Click on [Start the Blender]!'


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
