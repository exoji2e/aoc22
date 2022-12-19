#!/usr/bin/python3
import sys, time, datetime
sys.path.extend(['..', '.'])
from collections import *
from runner import main, get_commands
from utils import *
def get_day(): return 19
def get_year(): return 2022

MP = {
    'ore': 0,
    'clay': 1,
    'obsidian': 2,
    'geode': 3,
}


def parseRob(elem):
    cost = elem.split('costs')[1]
    vs = [0]*3
    for x in cost.split('and'):
        cnt, kind = x.strip().split()
        E = MP[kind]
        vs[E] = int(cnt)
    return vs


def parse(v):
    # Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs 3 ore and 8 obsidian.
    bps = []
    for ln in get_lines(v):
        elems = ln.split(': ')[1].split('.')
        bp = [
            parseRob(elem) for elem in elems[:4]
        ]
        bps.append(bp)
    return bps


def add(rbs, material):
    return tuple([r + m for r, m in zip(rbs, material)])

def sub(mat, cost):
    return tuple(m - c for m, c in zip(mat, cost))

def inc(robs, i):
    lr = list(robs)
    lr[i] += 1
    return tuple(lr)


def solve(bp, L):
    DP = {}

    def opt(ra, rb, rc, rd, ma, mb, mc, t):
        if t <= 0: return 0
        T = ra, rb, rc, rd, ma, mb, mc, t
        if T in DP:
            return DP[T]
        best = 0
        geo = rd
        robs = ra, rb, rc, rd
        mat = ma, mb, mc
        for i in range(4)[::-1]:
            mat2 = sub(mat, bp[i])
            if min(mat2) >= 0:
                ra2, rb2, rc2, rd2 = inc(robs, i)
                ma2, mb2, mc2 = add(robs, mat2)
                best = max(best,
                    geo + opt(ra2, rb2, rc2, rd2, ma2, mb2, mc2, t - 1)
                )
                if i >= 2:
                    DP[T] = best
                    return best
        ma2, mb2, mc2 = add(robs, mat)
        best = max(best,
            geo + opt(ra, rb, rc, rd, ma2, mb2, mc2, t - 1)
        )
        DP[T] = best
        return best

    return opt(1, 0, 0, 0, 0, 0, 0, L)



def p1(v):
    bps = parse(v)
    ans = 0
    for i, bp in list(enumerate(bps)):
        sc = solve(bp, 24)
        ans += (i+1)*sc
        print(i+1, sc, (i+1)*sc, ans)
    return ans

def p2(v):
    bps = parse(v)
    ans = 1
    for i, bp in list(enumerate(bps))[:3]:
        sc = solve(bp, 32)
        ans *= sc
        print(i+1, sc, ans)
    return ans


if __name__ == '__main__':
    options = get_commands()
    print('Commands:', options)
    main(get_year(), get_day(), p1, p2, options, FILE=__file__)
