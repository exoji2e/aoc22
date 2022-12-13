#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 13
def get_year(): return 2022

def compare(a, b):
    if type(a) == list and type(b) == int:
        return compare(a, [b])
    if type(a) == int and type(b) == list:
        return compare([a], b)
    if type(a) == int and type(b) == int:
        return a - b
    la = len(a)
    lb = len(b)
    for aa, bb in zip(a, b):
        v = compare(aa, bb)
        if v != 0: return v
    return la - lb


def p1(v):
    chunks = get_chunks(v)
    ans = 0
    for i, chunk in enumerate(chunks):
        L1, L2 = eval(chunk[0]), eval(chunk[1])
        if compare(L1, L2) < 0: ans += i
    return ans

def p2(v):
    chunks = get_chunks(v)
    divs = [[[2]], [[6]]]
    lst = []
    for i, chunk in enumerate(chunks):
        L1, L2 = eval(chunk[0]), eval(chunk[1])
        lst.append(L1)
        lst.append(L2)
    l1, l2 = 1, 2
    for l in lst:
        if compare(divs[0], l) > 0: l1 += 1
        if compare(divs[1], l) > 0 : l2 += 1
    return l1*l2


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
