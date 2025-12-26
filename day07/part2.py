from shared.utils import parse_grid
from collections import defaultdict

def solve(v):
    g=parse_grid(v); R,C=len(g),len(g[0]); ct, tt = {g[0].index('S'): 1}, 0
    for r in range(1, R):
        nxt = defaultdict(int)
        for c, n in ct.items():
            if not(0 <= c < C): tt += n
            elif g[r][c] == '^': nxt[c-1] += n; nxt[c+1] += n
            else: nxt[c] += n
        ct = nxt
    return tt + sum(ct.values())
