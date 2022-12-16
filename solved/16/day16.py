#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 16
def get_year(): return 2022

def parse(ln):
    # Valve SY has flow rate=23; tunnel leads to valve CS
    arr = ln.replace('=', ' ').replace(';', ' ').replace(', ',',').split()
    curr = arr[1]
    rate = int(arr[5])
    nbrs = arr[-1].split(',')
    return curr, rate, nbrs

def buildMaps(valves):
    chs = {lbl : ch for lbl, _, ch in valves}
    lb2rate = {lbl : r for lbl, r, _ in valves}
    lb2id = {}
    for lb, r, _ in valves:
        if r: lb2id[lb] = len(lb2id)
    return chs, lb2rate, lb2id

DP = {}
def opt(mask, lb, time):
    if time <= 0: return 0
    T = mask, lb, time
    if T in DP:
        return DP[T]
    alt = 0
    if lb in lb2id and (mask & (1<<lb2id[lb])) != 0:
        rate = lb2rate[lb]
        alt = max(alt, rate*(time - 1) + opt(mask ^ (1<<lb2id[lb]), lb, time - 1))
    for ch in chs[lb]:
        alt = max(alt, opt(mask, ch, time - 1))
    DP[T] = alt
    return alt


# not 2636
def p1(v):
    lns = get_lines(v)
    valves = [parse(ln) for ln in lns]
    global chs, lb2rate, lb2id, DP
    chs, lb2rate, lb2id = buildMaps(valves)
    L = len(lb2id)
    DP = {}
    mask = (1<<L) - 1
    return opt(mask, 'AA', 30)

def partitions(L):
    for p in range(1<<L):
        a, b = 0, 0
        for i in range(L):
            if p & (1<<i):
                a |= 1<<i
            else:
                b |= 1<<i
        yield a, b

def p2(v):
    lns = get_lines(v)
    valves = [parse(ln) for ln in lns]
    global chs, lb2rate, lb2id, DP
    chs, lb2rate, lb2id = buildMaps(valves)
    DP = {}
    best = 0
    for i, (a, b) in enumerate(partitions(len(lb2id))):
        alt = opt(a, 'AA', 26) + opt(b, 'AA', 26)
        best = max(best, alt)
    return best


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
