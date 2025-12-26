def solve(v, pos=50):
    z = 0
    for l in v.strip().splitlines():
        d, am, st = l[0], int(l[1:]), pos
        if d == 'R':
            pos += am
            z += (pos // 100) - (st // 100)
        else:
            pos -= am
            z += ((st - 1) // 100) - ((pos - 1) // 100)
    return z
