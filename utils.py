import re

# Grids
def grid4n(r, c):
    return [(r-1, c), (r, c-1), (r, c+1), (r+1, c)]
def grid8n(r, c):
    o = []
    for rr in range(r-1, r+2):
        for cc in range(c-1, c+2):
            if (rr, cc) != (r, c):
                o.append((rr, cc))
    return o

def filter_coords(coords, R, C):
    out = []
    for r, c in coords:
        if r < 0 or r >= R:
            continue
        if c < 0 or c >= C:
            continue
        out.append((r, c))
    return out

def grid4nf(r, c, R, C):
    return filter_coords(grid4n(r, c), R, C)
def grid8nf(r, c, R, C):
    return filter_coords(grid8n(r, c), R, C)

def printCoords(D, LIMIT=500):
    coords = list(D.keys())
    mnx = min(coords)[0]
    mny = min(coords, key=lambda c: c[1])[1]
    mxx = max(coords)[0]
    mxy = max(coords, key=lambda c: c[1])[1]
    if mxx - mnx >= LIMIT or mxy - mny >= LIMIT:
        print(D)
        return
    dx = max(mxx - mnx + 3, 10)
    dy = max(mxy - mny + 3, 10)
    G = [['.' for _ in range(dx)] for _ in range(dy)]
    for (x, y), v in D.items():
        G[mxy - y + 1][x - mnx + 1] = str(v)
    print('\n'.join(''.join(ln) for ln in G))
    print('----------------------')


# String parsing

def exact_match(pattern, s):
    return re.match('^' + pattern + '$', s) != None

def get_chunks(v):
    return [ch.split('\n') for ch in v.split('\n\n')]

def get_ints(v):
    return [int(x) for x in v.split()]

def get_lines(data):
    return data.strip('\n').split('\n')

def multi_split(s, schars):
    out = []
    curr = ''
    for c in s:
        if c in schars:
            if curr:
                out.append(curr)
                curr = ''
        else:
            curr += c
    if curr: out.append(curr)
    return out

def lazy_ints(arr):
    out = []
    for v in arr:
        if is_int(v):
            out.append(int(v))
        else:
            out.append(v)
    return out




def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

# VM
class VM:
    def __init__(self, reg, prog, instr_fn):
        self.reg = reg
        self.prog = prog
        self.instr_fn = instr_fn

        self.i = 0
        self.seen = set()
        self.running = True

    def err(self, tag, *strs):
        print('[VM: {}]'.format(tag), *strs)

    def still_running(self):
        i = self.i
        if i >= len(self.prog):
            self.running = False
        if i < 0:
            self.err('state', 'i < 0: {}'.format(i))
            self.running = False
        return self.running

    def step(self):
        if not self.running:
            self.err('step', 'calling step after termination')
            return
        if not self.still_running():
            return
        i = self.i
        instr = self.prog[i]
        self.i += self.instr_fn(self, instr)
        self.seen.add(i)

    def exec(self):
        while self.running:
            self.step()


def print_stats(v):
    lines = get_lines(v)
    print('INPUT[:10]:')
    for line in lines[:10]:
        print('> ' + line)
    if len(lines) > 10:
        print('...')
    tot_tokens = 0
    int_tokens = 0
    for line in lines:
        for tok in line.split():
            tot_tokens += 1
            if is_int(tok):
                int_tokens += 1
    print('lines: {}, tokens: {}, int_tokens: {}'.format(
        len(lines), tot_tokens, int_tokens))