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

    results = []
    for i, city in enumerate(arr):
        if i >= k:
            break
        # Don't place pylon here...
        no_pylon = pylons_internal(d, k, arr[i + 1:])
        # *Can* we place a pylon here?
        pylon = sys.maxsize
        if city == 1:
            pylon = pylons_internal(d, k - 1, arr[i + 1:]) + 1
        result =min(no_pylon, pylon)
        d[key] = result
        results.append(result)

    return min(results)


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
    hypothesis.strategies.lists(hypothesis.strategies.booleans(), min_size=1)
)
def test_zero_pylons(a):
    '''0 pylons will not suffice.'''
    cities = [1 if b else 0 for b in a]
    assert pylons(0, cities) == -1

@hypothesis.given(
    hypothesis.strategies.integers(min_value=1)
)
def test_electrify_every_city(n):
    '''If there are as many pylons as cities, there is a solution.'''
    cities = [1] * n
    assert pylons(len(cities), cities) > 0
