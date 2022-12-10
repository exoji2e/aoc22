#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return datetime.date.today().day
def get_year(): return 2022

def p1(v):
    lns = get_lines(v)
    chunks = v.split('\n\n')
    ans = 0
    for ln in lns:
        ans += 1
    return ans

def p2(v):
    return p1(v)


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
