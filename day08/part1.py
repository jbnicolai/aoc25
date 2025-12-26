from shared.utils import UnionFind, parse_pts

def gp(p): return sorted(((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2, i, j) for i, p1 in enumerate(p) for j, p2 in enumerate(p[i+1:], i+1))

def solve(v, limit=1000):
    pts = parse_pts(v); n = len(pts); dsu, ct = UnionFind(n), 0
    for _, i, j in gp(pts):
        if ct >= limit: break
        if dsu.union(i, j): ct += 1
    s = sorted([dsu.size[i] for i in range(n) if dsu.parent[i] == i], reverse=True)
    return s[0] * s[1] * s[2]

TEST_KWARGS, REAL_KWARGS = {'limit': 9}, {'limit': 740}
