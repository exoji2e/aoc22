#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 20
def get_year(): return 2022

def pL(c):
    print([v for _, v in c])

def mix(circ):
    L = len(circ)
    SZ = L - 1
    for i in range(L):
        for j in range(L):
            if i == circ[j][0]:
                break
        C = circ.pop(j)
        _, dt = C
        iP = (j + dt)%SZ
        circ.insert(iP, C)
    return circ

def calcAns(circ, L):
    pos0 = [i for i, (k, v) in enumerate(circ) if v == 0][0]
    return sum(circ[(pos0 + delta)%L][1] for delta in [1000, 2000, 3000])


def p1(v):
    lns = [int(x) for x in get_lines(v)]
    circ = list(enumerate(lns))
    circ = mix(circ)
    return calcAns(circ, len(lns))

def p2(v):
    MUL = 811589153
    lns = [int(x)*MUL for x in get_lines(v)]
    circ = list(enumerate(lns))
    for _ in range(10):
        circ = mix(circ)
    return calcAns(circ, len(lns))


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
