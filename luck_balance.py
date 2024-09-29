
sample_0 = [[5, 1], [2, 1], [1, 1], [8, 1], [10, 0], [5, 0]]

def recurse(m, k, c):
    if not c:
        return 0
    key = (k, len(c))
    if key in m:
        return m[key]
    if k == 0:
        result = sum([v for v, important in c if not important]) + sum([-v for v, important in c if important])
        m[key] = result
        return result
    v, important = c[0]
    if not important:
        return v + recurse(m, k, c[1:])
    x = v + recurse(m, k - 1, c[1:])
    y = recurse(m, k, c[1:]) - v
    result = max(x, y)
    m[key] = result
    return result

def luckBalance(k, c):
    m = {}
    return recurse(m, k, c)

print(luckBalance(3, sample_0))

sample_02 = [[5, 1], [4, 0], [6, 1], [2, 1], [8, 0]]

print(luckBalance(2, sample_02))
