'''https://www.hackerrank.com/challenges/luck-balance/problem'''


# "m" contains memoized subproblems.
# "k" is, per HackerRank, "the number of important contests Lena can lose."
# "c" is the remaining contests (i.e. some tail of the initial array).
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
        # We can lose this contest with impunity.
        return v + recurse(m, k, c[1:])
    # "If Lena wins the contest, her luck balance will decrease by L[i];
    # if she loses it, her luck balance will increase by L[i]."
    if_lose = v + recurse(m, k - 1, c[1:])
    if_win = recurse(m, k, c[1:]) - v
    result = max(if_lose, if_win)
    m[key] = result
    return result

# pylint: disable=C0103
def luckBalance(k, c):
    '''Memoized implementation starts with 0 memos.'''
    m = {}
    return recurse(m, k, c)

# Sample 0
assert luckBalance(3, [[5, 1], [2, 1], [1, 1], [8, 1], [10, 0], [5, 0]]) == 29

# Sample 1
assert luckBalance(2, [[5, 1], [4, 0], [6, 1], [2, 1], [8, 0]]) == 21
