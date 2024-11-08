'''
https://www.hackerrank.com/challenges/journey-to-the-moon/problem
'''

import collections
import itertools

import pytest

# pylint: disable=C0103
def journeyToMoon(pairs) -> int:
    '''
    Turn the list of pairs into an adjacency matrix. Compute
    the disjoint sets by the conventional algorithm.
    '''
    adjacency = collections.defaultdict(list)
    astronauts = set()
    for p in pairs:
        u, v = p
        # There's no functional reason for this.
        # It makes debugging more legible.
        if u > v:
            u, v = v, u
        adjacency[u].append(v)
        # Make sure we know how many astronauts there are.
        # TODO Are there singletons?
        astronauts.update(p)

    roots = {v: v for v in astronauts}

    def find_root(v):
        while roots[v] != v:
            v, roots[v] = roots[v], roots[roots[v]]
        return v

    disjoint_sets = { v: set([v]) for v in astronauts }

    for parent, children in adjacency.items():
        for child in children:
            parent_root, child_root = find_root(parent), find_root(child)
            if parent_root == child_root:
                continue
            roots[child] = parent_root
            disjoint_sets[parent].update(disjoint_sets[child])
            disjoint_sets.pop(child)

    population_sizes = [len(s) for s in disjoint_sets.values()]

    combinations = itertools.combinations(population_sizes, 2)
    return sum(x * y for x, y in combinations)

_SAMPLES = [
    ([(0, 1), (2, 3), (0, 4)], 6)
]

@pytest.mark.parametrize("pairs, expected", _SAMPLES)
def test_journey(pairs, expected: int):
    '''
    Parameterized test of the journey to the moon!
    '''
    actual = journeyToMoon(pairs)
    assert actual == expected
