'''
https://www.hackerrank.com/challenges/coin-change/problem
'''

# pylint: disable=C0116
def coin_change_internal(d: dict, n: int, c: list[int]):
    assert n > -1
    if n == 0:
        return 1
    if not c:
        return 0
    key = (len(c), n)
    if key in d:
        return d[key]
    result = 0
    uses = 0
    while uses * c[0] <= n:
        result += coin_change_internal(d, n - uses * c[0], c[1:])
        uses += 1
    assert n not in d
    d[key] = result
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

assert getWays(10, [5]) == 1
assert getWays(10, [5, 3]) == 1
assert getWays(16, [2, 4, 8]) == 9
assert getWays(100, [25, 50, 33, 34]) == 4

# Sample 0
assert getWays(4, [1, 2, 3]) == 4

# Sample 1
assert getWays(10, [2, 5, 3, 6]) == 5

# Test Case 2 96190959
print(getWays(166, [5, 37, 8, 39, 33, 17, 22, 32, 13, 7, 10, 35, 40, 2, 43, 49, 46, 19, 41, 1, 12, 11, 28])) # == 96190959

# Test Case 6
print(getWays(5, [6, 5]))
print(getWays(15, [10, 6, 5, 4, 2]))
print(getWays(15, [49, 22, 45, 6, 11, 20, 30, 10, 46, 8, 32, 48, 2, 41, 43, 5, 39, 16, 28, 44, 14, 4, 27, 36]))

# Test Case 10 3542323427
print(getWays(250, [8, 47, 13, 24, 25, 31, 32, 35, 3, 19, 40, 48, 1, 4, 17, 38, 22, 30, 33, 15, 44, 46, 36, 9, 20, 49]))