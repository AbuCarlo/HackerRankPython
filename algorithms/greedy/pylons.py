'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''

import hypothesis
import sys

import hypothesis.statistics
import hypothesis.strategies


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
        result = pylons_internal(d, k, arr[i + 1:])
        # *Can* we place a pylon here?
        if city == 1:
            result = min(result, pylons_internal(d, k - 1, arr[i + 1:]) + 1)
        d[key] = result

    return -1


def pylons(k: int, arr: list[int]) -> int:
    '''Use greedy algorithm with "memoization'''
    d = {}
    result = pylons_internal(d, k, arr)
    return result if result < sys.maxsize else -1

# pytest .\algorithms\greedy\pylons.py

def test_empty_array():
    '''For any k, an empty array is possible. Randomize!'''
    assert pylons(10, []) == 0 # 0 pylons are necessary to electrify an empty array.

def test_samples():
    '''samples from problem statement'''
    assert pylons(6, [0, 1, 1, 1, 1, 0]) == 2 # Sample 0 from the problem description

@hypothesis.given(
    hypothesis.strategies.integers(min_value=1, max_value=100),
)
def test_zero_pylons(p):
    '''0 pylons will not suffice.'''
    assert pylons(0, [0] * p) == -1
