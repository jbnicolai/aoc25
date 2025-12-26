from shared.utils import parse_graph_adj

def count_paths(g, s, e, m):
    if s == e: return 1
    if s not in m: m[s] = sum(count_paths(g, n, e, m) for n in g[s])
    return m[s]

def solve(v): return count_paths(parse_graph_adj(v), 'you', 'out', {})
