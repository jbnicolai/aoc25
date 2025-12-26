import bisect
from shared.utils import parse_range_list

def solve(v):
    rs = parse_range_list(v)
    if not rs: return 0
    mx, mn = max(r[1] for r in rs), min(r[0] for r in rs)
    cands = [v for ln in range(1, len(str(mx))//2 + 1) for i in range(10**(ln-1), 10**ln) if mn <= (v := int(str(i)*2)) <= mx]
    st, en = sorted(r[0] for r in rs), sorted(r[1] for r in rs)
    return sum(c * (bisect.bisect_right(st, c) - bisect.bisect_left(en, c)) for c in cands)
