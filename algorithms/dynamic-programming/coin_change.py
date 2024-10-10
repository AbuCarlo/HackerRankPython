
def coin_change_internal(d: dict, n: int, c: list[int]):
    if n == 0:
        return 1
    if n in d:
        return d[n]
    

# pylint: disable=C0103
def getWays(n: int, c: list[int]):
    d = {}
    c.sort(reverse=True)
    return coin_change_internal(d, n, c)
