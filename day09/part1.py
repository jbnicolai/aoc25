from shared.utils import parse_pts

def solve(v):
    pts, mx = parse_pts(v), 0
    for i, p1 in enumerate(pts):
        for j, p2 in enumerate(pts[i+1:], i+1):
            mx = max(mx, (abs(p1[0]-p2[0])+1) * (abs(p1[1]-p2[1])+1))
    return mx
