'''
https://www.hackerrank.com/challenges/coin-change/problem
'''

# pylint: disable=C0116
def coin_change_internal(d: dict, n: int, c: list[int]):
    if n == 0:
        return 1
    if not c:
        return 0
    if n in d:
        return d[n]
    result = 0
    for i, denomination in enumerate(c):
        for uses in range(1, n // denomination + 1):
            result += coin_change_internal(d, n - uses * denomination, c[i + 1:])
    d[n] = result
    return result


# pylint: disable=C0103
def getWays(n: int, c: list[int]):
    '''memoized implementation of recursive greedy algorithm'''
    d = {}
    c.sort(reverse=True)
    return coin_change_internal(d, n, c)

# There is only way to count out 0, whatever the coins.
assert getWays(0, [1, 2, 3]) == 1

# If all the coins are too big, the answer must be 0.
assert getWays(1, [2]) == 0

assert getWays(5, [5]) == 1

assert getWays(2, [1]) == 1

# Sample 0
assert getWays(4, [1, 2, 3]) == 4

# Sample 1
assert getWays(10, [2, 5, 3, 6]) == 5
