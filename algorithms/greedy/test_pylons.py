'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''

import pytest

# pylint: disable=C0116
def pylons_internal(d: dict, i: int, j: int, k: int, a: list[int]) -> int:
    while j < len(a) and a[j] == 0:
        j += 1
    if j == len(a):
        return None if j - i > k else 0
    if j - i > 2 * k - 1:
        return None
    key = (i, j)
    if key in d:
        return d[key]
    yes = pylons_internal(d, j, j + 1, k, a)
    # If we place a pylon here, and still have no
    # solution, there's no point in proceeding.
    # Obviously it would be even worse *not*
    # to place a pylon here.
    if yes is None:
        return None
    no = pylons_internal(d, i, j + 1, k, a)
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
    '''
    How many pylons do we have to place in order for every city to have electricity?

    :param k: a city must be at a distance < k from a pylon
    :param a: a list of cities, 1 denoting pylon-readiness
    :return: the smallest possible number of pylons, or -1 for an infeasible problem
    '''
    ones = [i for i, city in enumerate(a) if city]
    if not ones or ones[0] > k or ones[-1] < len(a) - k - 1:
        return -1
    for i, city in enumerate(ones[:-1]):
        if ones[i + 1] - city > 2 * k - 1:
            return -1
    d = {}
    for i in reversed(ones):
        if i <= k:
            continue
        pylons_internal(d, i, i + 1, k, a)

    solutions = []
    for i in ones:
        if i > k:
            break
        solution = pylons_internal(d, i, i + 1, k, a)
        # Add 1 for the pylon at a[i]
        if solution is not None:
            solutions.append(solution + 1)
    return min(solutions) if solutions else -1

# pytest .\algorithms\greedy\pylons.py

samples = [
    # "Example" from problem description
    (3, [0, 1, 1, 1, 0, 0, 0], -1),
    # Sample and "Sample 0" from "Run Code"
    (2, [0, 1, 1, 1, 1, 0], 2),
    # Sample 1
    (2, [0, 1, 0, 0, 0, 1, 0], -1),
    (3, [0, 1, 0, 0, 0, 1, 1, 1, 1, 1], 3)
]

@pytest.mark.parametrize("k,a,expected", samples)
def test_samples(k: int, a: list[int], expected: int):
    assert pylons(k, a) == expected

testdata = [
    (4, 28),
    (12, 1206),
    (15, 6864),
    # Overflows the stack.
    (16, 6),
    # Returns the wrong answer.
    (19, 17901)
]

@pytest.mark.parametrize("i,expected", testdata)
def test_test_cases(i: tuple[int, int], expected: tuple[int, int]):
    '''Run test cases from dowloaded input files'''
    path = f'algorithms/greedy/pylons-inputs/input{i:02d}.txt'
    with open(path, 'r', encoding='UTF-8') as f:
        size, k = f.readline().rstrip().split(' ')
        a = [int(s) for s in f.readline().rstrip().split(' ')]
        assert len(a) == int(size)
        assert pylons(int(k), a) == expected

def test_performance(benchmark):
    '''Test performance to achieve full score.'''
    with open('algorithms/greedy/pylons-inputs/input04.txt', 'r', encoding='UTF-8') as f:
        _, k = f.readline().rstrip().split(' ')
        a = [int(s) for s in f.readline().rstrip().split(' ')]
        benchmark(pylons, int(k), a)
