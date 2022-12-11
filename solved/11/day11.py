#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 11
def get_year(): return 2022

def parse(v):
    chunks = get_chunks(v)
    mItems = defaultdict(list)
    mTest = {}
    mOp = {}
    for chunk in chunks:
        mId = int(chunk[0].split()[-1][:-1])
        items = [x for x in lazy_ints(chunk[1].replace(',',' ').split()) if type(x) == int]
        mItems[mId] = items
        mOp[mId] = chunk[2].split('=')[1]
        div = lazy_ints(chunk[3].split())[-1]
        tTrue = lazy_ints(chunk[4].split())[-1]
        tFalse = lazy_ints(chunk[5].split())[-1]
        mTest[mId] = (div, tTrue, tFalse)
    return mItems, mTest, mOp

def evalOp(op, old):
    return eval(op.replace('old', str(old)))

def p1(v):
    mItems, mTest, mOp = parse(v)
    c = Counter()
    L = len(mItems)
    for rnd in range(20):
        for i in range(L):
            for item in mItems[i]:
                c[i] += 1
                nItem = evalOp(mOp[i], item)
                nItem = nItem//3
                d, t, f = mTest[i]
                if nItem % d == 0:
                    mItems[t].append(nItem)
                else:
                    mItems[f].append(nItem)
            mItems[i] = []
    v = sorted(c.values())
    return v[-1]*v[-2]

def mul(v):
    p = 1
    for x in v: p *= x
    return p

def p2(v):
    mItems, mTest, mOp = parse(v)
    c = Counter()
    L = len(mItems)
    MOD = mul([d for d, _, _ in mTest.values()])
    for rnd in range(1, 10001):
        if rnd % 1000 == 0:
            print(rnd/10000)
        for i in range(L):
            for item in mItems[i]:
                c[i] += 1
                nItem = evalOp(mOp[i], item)
                nItem = (nItem%MOD)
                d, t, f = mTest[i]
                if nItem % d == 0:
                    mItems[t].append(nItem)
                else:
                    mItems[f].append(nItem)
            mItems[i] = []
    v = sorted(c.values())
    return v[-1]*v[-2]
    return p1(v)


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
