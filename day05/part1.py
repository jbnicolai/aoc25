from shared.utils import merge_ranges, extract_ints

def pr(ls): return [(int(p[0]), int(p[1])) for l in ls if (p:=l.strip().split('-')) and len(p)==2]

def solve(v):
    s = v.strip().split('\n\n')
    mr = merge_ranges(pr(s[0].splitlines()))
    return sum(1 for x in extract_ints(s[1]) if any(st <= x <= en for st, en in mr))
