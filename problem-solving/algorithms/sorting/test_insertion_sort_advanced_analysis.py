'''
https://www.hackerrank.com/challenges/insertion-sort/problem
'''

import collections
from collections.abc import Iterable

import hypothesis
import hypothesis.strategies
import pytest

class _Node():
    def __init__(self, value):
        self.value = value
        self.count = 0
        self.size = 1
        self.left = None
        self.right = None
        
    def addLeftChild(self, node):
        assert self.left is None
        self.left = node
        if node is not None:
            self.size += node.size
    
    def addRightChild(self, node):
        assert self.right is None
        self.right = node
        if node is not None:
            self.size += node.size


def create_bst(l: list[int]):
    assert l is not None
    assert len(l) > 0
    
    values = list(sorted(set(l)))

    def create_bst_internal(i: int, j: int):
        assert j >= i
        if j == i:
            return None
        if j - i == 1:
            print(f'Node({values[i]})')
            return _Node(values[i])
        midpoint = (j + i) // 2
        print(f'Node({values[midpoint]})')
        root = _Node(values[midpoint])
        left = create_bst_internal(i, midpoint)
        right = create_bst_internal(midpoint + 1, j)
        root.addLeftChild(left)
        root.addRightChild(right)
        assert root.size == j - i
        return root

    bst = create_bst_internal(0, len(values))
    return bst

def traverse_bst(bst: _Node):
    '''
    Return a new list representing the depth-first
    traversal of the BST.
    '''
    l = []

    def traverse_bst_internal(n: _Node):
        if n is None:
            return
        traverse_bst_internal(n.left)
        l.append(n.value)
        traverse_bst_internal(n.right)

    traverse_bst_internal(bst)

    return l

# pylint: disable=C0103
def insertionSort(a):
    '''
    Count the number of swaps that an insertion sort on this
    array would require.

    :param a: an unsorted array to be sorted
    :returns: the number of swaps
    '''
    counts = collections.defaultdict(int)
    swaps = 0
    bst = create_bst(sorted(set(a)))

    for n in a:
        i = 0
        while bst[i] != n:
            # Does n have to swap with a larger value?
            if bst[i] is None:
                i = 2 * i + 1
                continue
            if n < bst[i]:
                swaps += counts[bst[i]]
            i = 2 * i + 1 if n < bst[i] else 2 * i + 2
        counts[n] += 1
    return swaps

# Stolen / learned from https://stackoverflow.com/a/73810689/476942
@hypothesis.strategies.composite
def unique_integers(draw):
    '''
    Return a list of unique integers.
    '''
    s = set()
    return draw(
        hypothesis.strategies.lists(
        hypothesis.strategies.integers(min_value=1, max_value=10000000)
        .filter(lambda n: n not in s)
        .map(lambda n: s.add(n) or n),
        min_size=1, max_size=10000
        )
    )

HACKER_RANK_SAMPLES = [
    ([1, 1, 1, 2, 2], 0),
    ([2, 1, 3, 1, 2], 4)
]

@pytest.mark.parametrize("a, expected", HACKER_RANK_SAMPLES)
def test_samples(a: list[int], expected: int):
    '''
    Test samples and test cases from HackerRank.
    '''
    assert insertionSort(a) == expected

@hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.integers(min_value=1, max_value=10000000), min_size=1, max_size=100000))
def test_sorted_input(l: list[int]):
    '''
    Any already-sorted list should require 0 swaps.
    '''
    l.sort()
    actual = insertionSort(l)
    assert actual == 0


@hypothesis.given(l=unique_integers())
def test_bst_round_trip(l):
    '''
    Verify that an BST represents the original array by
    depth-first traversal. The limits above are from the
    original problem. We've implemented the BST to *count*
    duplicates, so we have to start from an array of
    unique values.
    '''
    l.sort()
    bst = create_bst(l)
    actual = traverse_bst(bst)
    assert l == actual


_HACKER_RANK_SAMPLES = [
    # samples
    ([1, 1, 1, 2, 2], 0),
    ([2, 1, 3, 1, 2], 4)
    # test cases
]

@pytest.mark.parametrize("l,expected", _HACKER_RANK_SAMPLES)
def test_test_cases(l, expected):
    '''
    Samples and test cases from HackerRank
    '''
    actual = insertionSort(l)
    assert actual == expected
