#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 5
def get_year(): return 2022

def thing(ln):
    return 0

def parseStacks(chunk):
    lns = chunk[::-1]
    sz = max(map(int, lns[0].split()))
    stacks = [[] for _ in range(sz)]
    for ln in lns[1:]:
        for i in range(sz):
            if ln[i*4 + 1] != ' ':
                stacks[i].append(ln[4*i + 1])
    return stacks

def p1(v):
    chunks = get_chunks(v)
    stacks = parseStacks(chunks[0])
    moves = chunks[1]
    for move in moves:
        _, cnt, _, fr, _, to = lazy_ints(move.split())
        out = []
        for _ in range(cnt):
            out.append(stacks[fr-1].pop())
        stacks[to-1].extend(out)
    res = [s[-1] for s in stacks]
    return ''.join(res)

def p2(v):
    chunks = get_chunks(v)
    stacks = parseStacks(chunks[0])
    moves = chunks[1]
    for move in moves:
        _, cnt, _, fr, _, to = lazy_ints(move.split())
        out = []
        for _ in range(cnt):
            out.append(stacks[fr-1].pop())
        out = out[::-1]
        stacks[to-1].extend(out)
    res = [s[-1] for s in stacks]
    return ''.join(res)


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
