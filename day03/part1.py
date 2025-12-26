from bisect import bisect_left

def solve_max(s, k):
    n, res, cur, nd = len(s), 0, 0, k
    idx = [[] for _ in range(10)]
    for i, c in enumerate(s): idx[int(c)].append(i)
    for _ in range(k):
        for d in range(9, -1, -1):
            ids = idx[d]
            i_id = bisect_left(ids, cur)
            if i_id < len(ids) and ids[i_id] <= n - nd:
                res, cur, nd = res * 10 + d, ids[i_id] + 1, nd - 1
                break
    return res

def solve(v, k=2):
    return sum(solve_max(l.strip(), k) for l in v.strip().splitlines() if l.strip())
