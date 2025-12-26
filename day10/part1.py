import re, itertools
from shared.utils import extract_ints

def solve_sys(btns, tgt):
    L, B = len(tgt), len(btns)
    M = [[btns[c][r] for c in range(B)] + [tgt[r]] for r in range(L)]
    pr, pc = 0, []
    for c in range(B):
        if pr >= L: break
        p = next((r for r in range(pr, L) if M[r][c]), -1)
        if p == -1: continue
        M[pr], M[p] = M[p], M[pr]; pc.append(c)
        for r in range(L):
            if r != pr and M[r][c]:
                for col in range(c, B+1): M[r][col] ^= M[pr][col]
        pr += 1
    if any(M[r][B] for r in range(pr, L)): return float('inf')
    fv, mn = [c for c in range(B) if c not in pc], float('inf')
    for fvls in itertools.product([0, 1], repeat=len(fv)):
        x = [0]*B
        for i, v in enumerate(fvls): x[fv[i]] = v
        for i in range(len(pc)-1, -1, -1):
            cl = pc[i]
            x[cl] = (M[i][B] ^ sum(M[i][col] * x[col] for col in range(cl+1, B))) % 2
        mn = min(mn, sum(x))
    return mn

def solve(v):
    z = 0
    for l in v.strip().splitlines():
        if not (tm := re.search(r'\[([.#]+)\]', l)): continue
        tgt, btns = [1 if c=='#' else 0 for c in tm.group(1)], []
        for p in l.split(')'):
            if '(' in p:
                idx, vec = extract_ints(p.split('(')[1]), [0]*len(tm.group(1))
                for i in idx:
                    if 0 <= i < len(vec): vec[i] = 1
                btns.append(vec)
        r = solve_sys(btns, tgt)
        if r != float('inf'): z += r
    return z
