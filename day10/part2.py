import re; from shared.utils import extract_ints

def solve_ilp(btns, tgt):
    R, V = len(tgt), len(btns)
    M = [[float(btns[c][r]) for c in range(V)] + [float(tgt[r])] for r in range(R)]
    pr, pc = 0, []
    for c in range(V):
        if pr >= R: break
        p = next((r for r in range(pr, R) if abs(M[r][c]) > 1e-9), -1)
        if p == -1: continue
        M[pr], M[p] = M[p], M[pr]; pc.append(c)
        v = M[pr][c]
        for col in range(c, V + 1): M[pr][col] /= v
        for r in range(R):
            if r != pr and abs(M[r][c]) > 1e-9:
                f = M[r][c]
                for col in range(c, V + 1): M[r][col] -= f * M[pr][col]
        pr += 1
    if any(abs(M[r][V]) > 1e-9 for r in range(pr, R)): return float('inf')
    fv, dep, pbm = [c for c in range(V) if c not in pc], {}, {}
    for i, c in enumerate(pc):
        co = [(M[i][f], f) for f in fv if abs(M[i][f]) > 1e-9]
        dep[c] = (M[i][V], co)
        if co: pbm.setdefault(max(fv.index(f) for _,f in co), []).append(c)
    mn, f_bd = float('inf'), [int(min((tgt[r]//btns[f][r] for r in range(R) if btns[f][r]>0), default=100)) for f in fv]
    def bt(idx, s, x):
        nonlocal mn
        if s >= mn: return
        for p in pbm.get(idx-1, []):
            cs, co = dep[p]; val = cs - sum(c*x[f] for c,f in co)
            if abs(val-round(val)) > 1e-5 or val < -1e-5: return
        if idx == len(fv):
            ps = 0
            for p in pc:
                cs, co = dep[p]; val = cs - sum(c*x[f] for c,f in co)
                if abs(val-round(val)) > 1e-5 or val < -1e-5: return
                ps += int(round(val))
            mn = min(mn, s + ps); return
        for v in range(f_bd[idx] + 1): x[fv[idx]] = v; bt(idx+1, s+v, x)
    if not fv:
        ps = 0
        for p in pc:
            val = dep[p][0]
            if abs(val - round(val)) > 1e-5 or val < -1e-5: return float('inf')
            ps += int(round(val))
        return ps
    bt(0, 0, {}); return mn

def solve(v):
    z = 0
    for l in v.strip().splitlines():
        if not (tm := re.search(r'\[([.#]+)\]', l)): continue
        tj = extract_ints(re.search(r'\{([0-9,]+)\}', l).group(1)) if '{' in l else []
        btns = []
        for p in l.split(')'):
            if '(' in p:
                idx, vec = extract_ints(p.split('(')[1]), [0]*len(tm.group(1))
                for i in idx:
                    if 0 <= i < len(vec): vec[i] = 1
                btns.append(vec)
        r = solve_ilp(btns, tj)
        if r != float('inf'): z += r
    return z
