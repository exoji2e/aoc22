#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import run, run_samples, get_commands
from utils import *
def get_day(): return 2
def get_year(): return 2022

def getOwnScore(s):
    return s + 1

def getGameScore(a, b):
    if a == b: return 3
    if a == (b-1)%3: return 6
    return 0

def handFromGame(a, state):
    if state == 0:
        return (a - 1)%3
    if state == 1:
        return a
    if state == 2:
        return (a + 1)%3


def p1(v):
    lines = get_lines(v)
    sc = 0
    for l in lines:
        a, b = l.split()
        noA = ord(a) - ord('A')
        noB = ord(b) - ord('X')
        sc += getOwnScore(noB) + getGameScore(noA, noB)
    return sc


def p2(v):
    lines = get_lines(v)
    sc = 0
    for l in lines:
        a, b = l.split()
        noA = ord(a) - ord('A')
        state = ord(b) - ord('X')
        noB = handFromGame(noA, state)
        sc += getOwnScore(noB) + getGameScore(noA, noB)
    return sc


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
