from shared.utils import UnionFind, parse_pts
from day08.part1 import gp

def solve(v, limit=1e9):
    pts = parse_pts(v); dsu = UnionFind(len(pts))
    for d, i, j in gp(pts):
        if d > limit: break
        if dsu.union(i, j) and dsu.num_components == 1: return pts[i][0] * pts[j][0]
    return 0

REAL_KWARGS = {'limit': 1e9}
