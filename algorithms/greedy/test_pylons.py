'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''
import sys

import hypothesis
import hypothesis.statistics
import hypothesis.strategies

d = {}

# TODO Create a memo for (previous, position)
def pylons_internal(i: int, j: int, k: int, a: list[int]) -> int:
    while j < len(a) and a[j] == 0:
        j += 1
    if j == len(a):
        return None if j - i > k else 0
    if j - i > 2 * k - 1:
        return None
    key = (i, j)
    if key in d:
        return d[key]
    yes = pylons_internal(j, j + 1, k, a)
    # If we place a pylon here, and still have no
    # solution, there's no point in proceeding.
    # Obviously it would be even worse *not*
    # to place a pylon here.
    if yes is None:
        return None
    no = pylons_internal(i, j + 1, k, a)
    solution = None
    if no is None:
        solution = 1 + yes
    elif no <= yes:
        solution = no
    else:
        solution = 1 + yes
    d[key] = solution
    return solution

def pylons(k: int, a: list[int]) -> int:
    '''How many pylons do we to place in order for every city to have electricity?
    k: a city must be at a distance < k from a pylon
    a: a list of cities, 1 denoting pylon-readiness
    '''
    solution = sys.maxsize
    for i, e in enumerate(a):
        if i >= k:
            break
        if e == 0:
            continue
        s = pylons_internal(i, i + 1, k, a)
        if s is not None:
            solution = min(s + 1, solution)
    # print(f'Solutions for k = {k}, a = {a}: {solutions}')
    return solution if solution < sys.maxsize else -1


# pytest .\algorithms\greedy\pylons.py

def test_samples():
    '''samples from HackerRank"'''
    # "Example" from problem description
    assert(pylons(3, [0, 1, 1, 1, 0, 0, 0])) == -1
    # "Sample"
    assert pylons(2, [0, 1, 1, 1, 1, 0]) == 2
    # samples test cases from "Run Code"
    assert pylons(2, [0, 1, 1, 1, 1, 0]) == 2
    assert pylons(2, [0, 1, 0, 0, 0, 1, 0]) == -1
    assert pylons(3, [0, 1, 0, 0, 0, 1, 1, 1, 1, 1]) == 3


def test_test_cases():
    '''Run test cases from dowloaded input files'''
    for t, expected in [(4, 28), (12, 1206)]:
        path = f'algorithms/greedy/pylons-inputs/input{t:02d}.txt'
        with open(path, 'r', encoding='UTF-8') as f:
            _, k = f.readline().rstrip().split(' ')
            a = [int(s) for s in f.readline().rstrip().split(' ')]
            assert pylons(int(k), a) == expected
            

# @hypothesis.given(
#     hypothesis.strategies.lists(hypothesis.strategies.booleans(), min_size=1, max_size=100)
# )
# def test_zero_pylons(a):
#     '''0 pylons will not suffice for any number of cities.'''
#     cities = [1 if b else 0 for b in a]
#     assert pylons(0, cities) == -1

# @hypothesis.given(
#     hypothesis.strategies.integers(min_value=1, max_value=100)
# )
# def test_electrify_every_city(n):
#     '''If there are as many pylons as cities, there is a solution.'''
#     cities = [1] * n
#     assert pylons(n, cities) > 0

