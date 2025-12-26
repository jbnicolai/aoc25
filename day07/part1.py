from shared.utils import parse_grid

def solve(v):
    g=parse_grid(v); R,C=len(g),len(g[0]); ac={g[0].index('S')}; sp=0
    for r in range(1, R):
        nxt = set()
        for c in ac:
            if 0 <= c < C:
                if g[r][c] == '^':
                    sp += 1; nxt |= {c-1, c+1}
                else: nxt.add(c)
        if not(ac := nxt): break
    return sp
