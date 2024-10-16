'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''

import itertools
import pytest

def pylons(k: int, a: list[int]) -> int:
    '''
    How many pylons do we have to place in order for every city to have electricity?

    :param k: a city must be at a distance < k from a pylon
    :param a: a list of cities, 1 denoting pylon-readiness
    :return: the smallest possible number of pylons, or -1 for an infeasible problem
    '''
    ones = [i for i, city in enumerate(a) if city]
    if not ones or ones[0] >= k or ones[-1] + k - 1 < len(a) -1:
        return -1
    for i, city in enumerate(ones[:-1]):
        if ones[i + 1] - city > 2 * k - 1:
            return -1
    # The optimal solution starting from the last city
    # that can have a pylon is, obviously, 1.
    d = {ones[-1]: 1}
    for i in reversed(ones[:-1]):
        solutions = []
        # The furthest pylon provides the optimal subsolution.
        for j in range(i + 2 * k -1, i, -1):
            if j in d:
                d[i] = d[j] + 1
                break

    solutions = []
    for i in itertools.takewhile(lambda i: i < k, ones):
        solutions.append(d[i])
    assert solutions
    return min(solutions)

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
    '''Examples from HackerRank's problem description'''
    assert pylons(k, a) == expected
    b = a.copy()
    b.reverse()
    assert pylons(int(k), b) == expected

testdata = [
    (4, 28),
    (12, 1206),
    (15, 6864),
    (16, 6),
    (19, 17901)
]

CURRENT_DIRECTORY = 'problem-solving/algorithms/greedy'

@pytest.mark.parametrize("i,expected", testdata)
def test_test_cases(i: tuple[int, int], expected: tuple[int, int]):
    '''Run test cases from dowloaded input files'''
    path = f'{CURRENT_DIRECTORY}/pylons-inputs/input{i:02d}.txt'
    with open(path, 'r', encoding='UTF-8') as f:
        size, k = [int(s) for s in f.readline().rstrip().split(' ')]
        a = [int(s) for s in f.readline().rstrip().split(' ')]
        assert len(a) == size
        assert pylons(k, a) == expected


@pytest.mark.parametrize('name', [f'input{i:02d}.txt' for i in [4, 16, 19]])
def test_performance(benchmark, name):
    '''Test performance to achieve full score.'''
    path = f'{CURRENT_DIRECTORY}/pylons-inputs/{name}'
    with open(path, 'r', encoding='UTF-8') as f:
        size, k = [int(s) for s in f.readline().rstrip().split(' ')]
        a = [int(s) for s in f.readline().rstrip().split(' ')]
        assert len(a) == size
        benchmark(pylons, int(k), a)
