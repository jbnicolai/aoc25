from shared.utils import parse_pts, DIRECTIONS_4

def solve(v):
    pts = parse_pts(v); n = len(pts)
    if n < 2: return 0
    xs, ys = set(), set()
    for x, y in pts: xs.update({x, x+1}); ys.update({y, y+1})
    sx, sy = sorted(xs), sorted(ys)
    xm, ym = {p: i for i, p in enumerate(sx)}, {p: i for i, p in enumerate(sy)}
    W, H = len(sx)-1, len(sy)-1; g = [[0]*W for _ in range(H)]
    for i in range(n):
        p1, p2 = pts[i], pts[(i+1)%n]
        x1, x2, y1, y2 = xm[p1[0]], xm[p2[0]], ym[p1[1]], ym[p2[1]]
        if y1 == y2:
            for c in range(min(x1,x2), max(x1,x2)+1):
                if 0<=c<W: g[y1][c]=1
        else:
            for r in range(min(y1,y2), max(y1,y2)+1):
                if 0<=r<H: g[r][x1]=1
    q = []
    for c in range(W):
        if not g[0][c]: g[0][c]=2; q.append((0,c))
        if not g[H-1][c]: g[H-1][c]=2; q.append((H-1,c))
    for r in range(H):
        if not g[r][0]: g[r][0]=2; q.append((r,0))
        if not g[r][W-1]: g[r][W-1]=2; q.append((r,W-1))
    idx = 0
    while idx < len(q):
        r, c = q[idx]; idx += 1
        for dr, dc in DIRECTIONS_4:
            nr, nc = r+dr, c+dc
            if 0<=nr<H and 0<=nc<W and not g[nr][nc]: g[nr][nc]=2; q.append((nr,nc))
    pref = [[0]*(W+1) for _ in range(H+1)]
    for r in range(H):
        for c in range(W): pref[r+1][c+1] = pref[r][c+1] + pref[r+1][c] - pref[r][c] + (1 if g[r][c]==2 else 0)
    mx = 0
    for i in range(n):
        for j in range(i+1, n):
            p1, p2 = pts[i], pts[j]
            x1, x2, y1, y2 = xm[min(p1[0],p2[0])], xm[max(p1[0],p2[0])], ym[min(p1[1],p2[1])], ym[max(p1[1],p2[1])]
            if pref[y2+1][x2+1] - pref[y1][x2+1] - pref[y2+1][x1] + pref[y1][x1] == 0:
                mx = max(mx, (sx[x2]-sx[x1]+1)*(sy[y2]-sy[y1]+1))
    return mx
