#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 21
def get_year(): return 2022

def getExpr(Monks):
    def opt(mnk):
        arr = Monks[mnk].split()
        if len(arr) == 1:
            return lazy_ints(arr)[0]
        assert len(arr) == 3
        m1, op, m2  = arr
        o1, o2 = opt(m1), opt(m2)
        return f'({o1} {op} {o2})'
    return opt('root')

def p1(v):
    lns = get_lines(v)
    mks = [ln.split(': ') for ln in lns]
    Monks = {k : v for k, v in mks}

    S = getExpr(Monks)
    return int(eval(S))


def p2(v):
    lns = get_lines(v)
    mks = [ln.split(': ') for ln in lns]
    Monks = {k : v for k, v in mks}
    Monks['root'] = Monks['root'].replace('+', '-')
    Monks['humn'] = 'humn'
    S = getExpr(Monks)
    def getVal(humn):
        return eval(S.replace('humn', str(humn)))
    h0 = getVal(0)
    lo = 0
    hi = 10**20
    while lo < hi:
        mid = (lo + hi)//2
        v = getVal(mid)
        if v*h0 > 0:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
