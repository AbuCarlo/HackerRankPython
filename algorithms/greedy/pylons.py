'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''

import sys

def pylons_internal(d: dict, k: int, arr: list[int]) -> int:
    '''Recursive implementation using dictionary to store subsolutions'''
    if not arr:
        # No more pylons are necessary.
        return 0
    if k == 0:
        return sys.maxsize
    key = (k, len(arr))
    if key in d:
        return d[key]

    for i, city in enumerate(arr):
        if i >= k:
            return sys.maxsize
        # Don't place pylon here...
        pylons_internal(d, k, arr[i:])
        # *Can* we place a pylon here?
        if city == 1:
            result = min(result, pylons_internal(d, k - 1, arr[i:]) + 1)
        d[key] = result

    return -1


def pylons(k: int, arr: list[int]) -> int:
    '''Use greedy algorithm with "memoization'''
    d = {}
    result = pylons_internal(d, k, arr)
    return result if result < sys.maxsize else -1

assert pylons(6, [0, 1, 1, 1, 1, 0]) == 2
