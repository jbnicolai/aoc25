from shared.utils import parse_grid, get_neighbors

def solve(v):
    g=parse_grid(v); R,C=len(g),len(g[0])
    return sum(1 for r in range(R) for c in range(C) if g[r][c]=='@' and sum(1 for nr,nc in get_neighbors(r,c,R,C,1) if g[nr][nc]=='@') < 4)
