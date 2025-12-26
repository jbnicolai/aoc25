from shared.utils import parse_grid, DIRECTIONS_8

def solve(v):
    g=parse_grid(v); R,C=len(g),len(g[0]); q, rm, ct = [], set(), {}
    for r in range(R):
        for c in range(C):
            if g[r][c]=='@':
                n=sum(1 for dr,dc in DIRECTIONS_8 if 0<=r+dr<R and 0<=c+dc<C and g[r+dr][c+dc]=='@')
                ct[(r,c)]=n
                if n<4: q.append((r,c)); rm.add((r,c))
    idx=0
    while idx<len(q):
        r,c=q[idx]; idx+=1
        for dr,dc in DIRECTIONS_8:
            nr,nc=r+dr,c+dc
            if (nr,nc) in ct and (nr,nc) not in rm:
                ct[(nr,nc)]-=1
                if ct[(nr,nc)]==3: rm.add((nr,nc)); q.append((nr,nc))
    return len(rm)
