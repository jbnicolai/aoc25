import sys, os, concurrent.futures as cf
from shared.utils import extract_ints

class Piece:
    def __init__(self, pid, s):
        def norm(c):
            mr, mc = min(r for r,c in c), min(c for r,c in c)
            return frozenset((r-mr, c-mc) for r,c in c)
        v = set()
        for _ in range(4):
            v.add(norm(s)); v.add(norm({(r,-c) for r,c in s}))
            s = {(c,-r) for r,c in s}
        self.pid = pid
        self.variants = [(x, max(r for r,c in x)+1, max(c for r,c in x)+1) for x in v if x]
        self.area, self.pd = len(next(iter(v))), sum(1 if (r+c)%2==0 else -1 for r,c in next(iter(v)))

def parse_input(content):
    sm, lines = {}, []
    for b in [b.strip() for b in content.split('\n\n') if b.strip()]:
        ls = b.splitlines()
        if ':' in ls[0]:
            pre = ls[0].split(':', 1)[0].strip()
            if 'x' in pre and pre.replace('x', '').isdigit(): lines.extend(ls)
            elif pre.isdigit(): sm[int(pre)] = Piece(int(pre), set((r,c) for r,row in enumerate(ls[1:]) for c,ch in enumerate(row) if ch=='#'))
            else: [lines.append(l) for l in ls if ':' in l and 'x' in l.split(':')[0]]
    return sm, lines

CACHE_MASKS = {}

def get_masks(pi, w, h):
    k = (tuple(p['pid'] for p in pi), w, h)
    if k in CACHE_MASKS: return CACHE_MASKS[k]
    gs, res = w * h, []
    for p_info in pi:
        p, ml = p_info['original_piece'], [[] for _ in range(w * h)]
        for v, vh, vw in p.variants:
            vm = sum(1 << (r*w+c) for r,c in v)
            for r0 in range(h-vh+1):
                for c0 in range(w-vw+1):
                    m, vpd, tmp = vm<<(r0*w+c0), 0, vm<<(r0*w+c0)
                    while tmp:
                        b = (tmp&-tmp).bit_length()-1; vpd += 1 if (b//w+b%w)%2==0 else -1; tmp &= tmp-1
                    for br, bc in v: ml[(r0+br)*w+(c0+bc)].append((m, vpd))
        res.append(ml)
    CACHE_MASKS[k] = res; return res

def solve_region(w, h, cts, sm):
    gs, pi = w * h, []
    ta = tpd = tp = max_h = max_w = 0
    for pid, c in enumerate(cts):
        if c > 0:
            p = sm[pid]; pi.append({'pid':pid, 'area':p.area, 'count':c, 'original_piece':p})
            ta += p.area*c; tpd += p.pd*c; tp += c
            for _, vh, vw in p.variants: max_h, max_w = max(max_h, vh), max(max_w, vw)
    if ta > gs: return 0
    if max_h > 0 and (w // max_w)*(h // max_h) >= tp: return 1
    pi.sort(key=lambda x: x['area'], reverse=True)
    gpd = 2*sum(1 for i in range(gs) if (i//w + i%w)%2==0) - gs
    tgp, tsk = gpd-tpd, gs-ta
    if abs(tgp) > tsk or (tsk-tgp)%2: return 0
    pms, memo = get_masks(pi, w, h), {}
    ml, mr = ((1<<gs)-1) & ~sum(1<<(r*w+w-1) for r in range(h)), ((1<<gs)-1) & ~sum(1<<(r*w) for r in range(h))
    def bt(m, cs, sk, cgp, are, cmn):
        if (m, cs) in memo: return memo[(m, cs)]
        if not are: return 1
        if abs(tgp-cgp) > (tsk-sk): return 0
        if sk < tsk:
            wasted, tu = 0, ~m & ((1<<gs)-1)
            while tu:
                low = tu & -tu; cp, tu = low, tu^low
                while 1:
                    g = ((cp>>w)|(cp<<w)|((cp&ml)<<1)|((cp&mr)>>1)) & tu
                    if not g: break
                    cp|=g; tu^=g
                if cp.bit_count() < cmn: wasted += cp.bit_count()
            if sk+wasted > tsk: return 0
        t = (~m & ((1<<gs)-1) & -(~m & ((1<<gs)-1))).bit_length()-1
        for i in range(len(pi)):
            if cs[i] > 0:
                pa, nmn = pi[i]['area'], cmn
                if pa == cmn and cs[i] == 1: nmn = min((pi[j]['area'] for j in range(len(pi)) if (cs[j] if j != i else 0) > 0), default=0)
                for pm, ppd in pms[i][t]:
                    if not (m & pm):
                        ncs = list(cs); ncs[i] -= 1
                        if bt(m | pm, tuple(ncs), sk, cgp, are-pa, nmn): return 1
        if sk < tsk:
            if bt(m | (1<<t), cs, sk+1, cgp + (1 if (t//w+t%w)%2==0 else -1), are, cmn): return 1
        memo[(m, cs)] = 0; return 0
    sys.setrecursionlimit(max(2000, gs + 500))
    return bt(0, tuple(p['count'] for p in pi), 0, 0, ta, pi[-1]['area'] if pi else 0)

def worker(a):
    try:
        dp, cp = a[0].split(':'); w, h = extract_ints(dp)
        return solve_region(w, h, extract_ints(cp), a[1])
    except: return 0

def solve(cont):
    sm, lns = parse_input(cont)
    with cf.ProcessPoolExecutor() as ex:
        res = list(ex.map(worker, [(l, sm) for l in lns]))
    return sum(1 for r in res if r)
