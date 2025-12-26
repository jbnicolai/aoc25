import bisect
from shared.utils import parse_range_list

def solve(v):
    rs = parse_range_list(v)
    if not rs: return 0
    mx, mn, cands = max(r[1] for r in rs), min(r[0] for r in rs), set()
    for ln in range(1, len(str(mx)) // 2 + 1):
        for i in range(10**(ln-1), 10**ln):
            s, cur = str(i), str(i) * 2
            while len(cur) <= len(str(mx)):
                val = int(cur)
                if val > mx: break
                if val >= mn: cands.add(val)
                cur += s
    st, en = sorted(r[0] for r in rs), sorted(r[1] for r in rs)
    return sum(c * (bisect.bisect_right(st, c) - bisect.bisect_left(en, c)) for c in sorted(cands))
