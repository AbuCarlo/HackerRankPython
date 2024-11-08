'''
https://www.hackerrank.com/challenges/journey-to-the-moon/problem
'''

import collections
import itertools

import pytest

# pylint: disable=C0103
def journeyToMoon(n: int, pairs) -> int:
    '''
    Disjoint sets algorithm, computing only the sizes of the sets.
    '''
    roots = list(range(n))

    def find_root(v):
        while roots[v] != v:
            v, roots[v] = roots[v], roots[roots[v]]
        return v

    disjoint_sets = [1] * n

    # pairs = [(u, v) if u < v else (v, u) for u, v in pairs]
    # pairs.sort()

    for parent, child in pairs:
        parent_root, child_root = find_root(parent), find_root(child)
        if parent_root == child_root:
            continue
        # We don't need to compare the sizes of the disjoint sets,
        # since they're both just integers.
        child_set = disjoint_sets[child_root]
        roots[child_root] = parent_root
        disjoint_sets[parent_root] += child_set
        disjoint_sets[child_root] = 0

    # This is faster than nested loops!
    combinations = itertools.combinations([size for size in disjoint_sets if size > 0], 2)
    result = sum(x * y for x, y in combinations)
    return result

_SAMPLES = [
    (5, [(0, 1), (2, 3), (0, 4)], 6),
    (4, [(0, 2)], 5),
    (10, [(0,2), (1,8), (1,4), (2,8), (2,6), (3,5), (6,9)], 23),
    (100, [(0, 11), (2, 4), (2, 95), (3, 48), (4, 85), (4, 95), (5, 67), (5, 83), (5, 42), (6, 76), (9, 31), (9, 22), (9, 55), (10, 61), (10, 38), (11, 96), (11, 41), (12, 60), (12, 69), (14, 80), (14, 99), (14, 46), (15, 42), (15, 75), (16, 87), (16, 71), (18, 99), (18, 44), (19, 26), (19, 59), (19, 60), (20, 89), (21, 69), (22, 96), (22, 60), (23, 88), (24, 73), (27, 29), (30, 32), (31, 62), (32, 71), (33, 43), (33, 47), (35, 51), (35, 75), (37, 89), (37, 95), (38, 83), (39, 53), (41, 84), (42, 76), (44, 85), (45, 47), (46, 65), (47, 49), (47, 94), (50, 55), (51, 99), (53, 99), (56, 78), (66, 99), (71, 78), (73, 98), (76, 88), (78, 97), (80, 90), (83, 95), (85, 92), (88, 99), (88, 94)], 3984)
]

@pytest.mark.parametrize("n, pairs, expected", _SAMPLES)
def test_journey(n, pairs, expected: int):
    '''
    Parameterized test of the journey to the moon!
    '''
    actual = journeyToMoon(n, pairs)
    assert actual == expected

def test_as_benchmark(benchmark):
    '''
    Using Pytest to improve this performance.
    '''
    n, pairs, expected = _SAMPLES[3]
    benchmark(test_journey, n, pairs, expected)
