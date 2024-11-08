'''
https://www.hackerrank.com/challenges/journey-to-the-moon/problem
'''

import collections
import itertools

import pytest

# pylint: disable=C0103
def journeyToMoon(n: int, pairs) -> int:
    '''
    Turn the list of pairs into an adjacency matrix. Compute
    the disjoint sets by the conventional algorithm.
    '''
    adjacency = collections.defaultdict(list)
    for p in pairs:
        u, v = p
        # There's no functional reason for this.
        # It makes debugging more legible.
        if u > v:
            u, v = v, u
        adjacency[u].append(v)

    roots = {a: a for a in range(n) }

    def find_root(v):
        while roots[v] != v:
            v, roots[v] = roots[v], roots[roots[v]]
        return v

    disjoint_sets = {v: 1 for v in range(n)}

    for parent in adjacency:
        for child in adjacency[parent]:
            parent_root, child_root = find_root(parent), find_root(child)
            if parent_root == child_root:
                continue
            # pylint: disable=C0301
            parent_set, child_set = disjoint_sets.get(parent_root, 0), disjoint_sets.get(child_root, 0)
            if parent_set < child_set:
                roots[parent_root] = child_root
                disjoint_sets[child_root] += parent_set
                disjoint_sets.pop(parent_root)
            else:
                roots[child_root] = parent_root
                disjoint_sets[parent_root] += child_set
                disjoint_sets.pop(child_root)

    combinations = itertools.combinations(disjoint_sets.values(), 2)
    return sum(x * y for x, y in combinations)

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
