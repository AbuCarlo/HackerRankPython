'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''

import hypothesis
import hypothesis.statistics
import hypothesis.strategies

def pylons_internal(previous: int, position: int, k: int, a: list[int]) -> int:     
    while position < len(a):
        if a[position] == 1:
            break
    if position - previous > k * 2:
        return -1
    emplace = pylons_internal(position, position + 1, k, a)
    dont_emplace = pylons_internal(previous, position + 1, k, a)
    if emplace == - 1:
        return dont_emplace + 1
    if dont_emplace == -1:
        return -1
    return min( + 1, dont_emplace)


def pylons(k: int, arr: list[int]) -> int:
    '''Use greedy algorithm with "memoization'''
    return pylons_internal(-k, 0, k, arr)

# pytest .\algorithms\greedy\pylons.py

@hypothesis.given(
    hypothesis.strategies.integers(min_value=1)
)
def test_empty_array(k):
    '''For any k, an empty array is possible. Randomize!'''
    assert pylons(k, []) == 0 # 0 pylons are necessary to electrify an empty array.

def test_samples():
    '''samples from "Run Code"'''
    assert pylons(6, [0, 1, 1, 1, 1, 0]) == 2
    assert pylons(2, [0, 1, 0, 0, 0, 1, 0]) == -1
    assert pylons(3, [0, 1, 0, 0, 0, 1, 1, 1, 1, 1]) == 3

@hypothesis.given(
    hypothesis.strategies.lists(hypothesis.strategies.booleans(), min_size=1)
)
def test_zero_pylons(a):
    '''0 pylons will not suffice for any number of cities.'''
    cities = [1 if b else 0 for b in a]
    assert pylons(0, cities) == -1

@hypothesis.given(
    hypothesis.strategies.integers(min_value=1)
)
def test_electrify_every_city(n):
    '''If there are as many pylons as cities, there is a solution.'''
    cities = [1] * n
    assert pylons(n, cities) > 0

