def solve(v, pos=50):
    z, dm = 0, {'R': 1, 'L': -1}
    for l in v.strip().splitlines():
        pos = (pos + dm[l[0]] * int(l[1:])) % 100
        if pos == 0: z += 1
    return z
