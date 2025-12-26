from shared.utils import merge_ranges
from day05.part1 import pr

def solve(v):
    return sum(e - s + 1 for s, e in merge_ranges(pr(v.strip().split('\n\n')[0].splitlines())))
