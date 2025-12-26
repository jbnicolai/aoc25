from shared.utils import extract_ints

def get_blocks(v):
    ls = v.splitlines(); g = [l.ljust(max(len(x) for x in ls)) for l in ls]
    sep = [-1] + [c for c in range(len(g[0])) if all(g[r][c] == ' ' for r in range(len(g)))] + [len(g[0])]
    for i in range(len(sep)-1):
        if sep[i+1]-sep[i] > 1: yield [r[sep[i]+1:sep[i+1]] for r in g]

def solve(v, p=1):
    z = 0
    for b in get_blocks(v):
        if p == 1: ns, op = extract_ints('\n'.join(b[:-1])), b[-1].strip()
        else:
            ns = [int(s) for c in range(len(b[0])) if (s := "".join(b[r][c] for r in range(len(b)) if b[r][c].isdigit()))]
            op = next(ch for r in b for ch in r if ch in '+*')
        res = 1 if op == '*' else 0
        for n in ns: res = res * n if op == '*' else res + n
        z += res
    return z
