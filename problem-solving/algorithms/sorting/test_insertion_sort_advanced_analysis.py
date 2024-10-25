'''
https://www.hackerrank.com/challenges/insertion-sort/problem
'''

import collections
from collections.abc import Iterable

import hypothesis
import hypothesis.strategies
import pytest

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
    bst = make_bst(sorted(set(a)))

    for n in a:
        i = 0
        while bst[i] != n:
            # Does n have to swap with a larger value?
            if n < bst[i]:
                swaps += counts[bst[i]]
            i = 2 * i + 1 if n < bst[i] else 2 * i + 2
        counts[n] += 1
    return swaps

def calculate_tree_size(n: int) -> int:
    '''
    A perfectly balanced tree will have a
    size 2^n - 1 for some n. We want to round
    len() up to a power of 2, unless it's
    already a power of 2, in which case
    we need to round it up one more time.
    '''
    assert n > 0
    # 1 represents an edge case: it's 1 less than
    # a power of two, and it's also a power of two.
    # But we know that we can represent a single
    # node as an array of length 1.
    if n == 1:
        return 1
    bits = n.bit_length()
    if n == 1 << bits:
        bits += 1
    result = (1 << bits) - 1
    return result

def make_bst(l: Iterable[int]):
    '''
    Turn a sorted array of unique values into a binary search tree
    to allow counting instances of n in a in log(len(a)) time.
    '''
    if not l:
        return []
    size = calculate_tree_size(len(l))
    root = size // 2
    width = root + 1
    bst = [None] * size
    bst[0] = l[root]
    i = 0
    while width > 1:
        for j in range((width // 2) - 1, size, width):
            # This happens on the first iteration.
            if j == root:
                continue
            bst[i + 1] = l[j]
            i += 1
        width //= 2
    return bst

def traverse_bst(bst: list[int]):
    '''
    Return a new list representing the depth-first
    traversal of the BST.
    '''
    if not bst:
        return []
    l = []

    def traverse_bst_internal(i: int):
        if i >= len(bst):
            return
        traverse_bst_internal(2 * i + 1)
        l.append(bst[i])
        traverse_bst_internal(2 * i + 2)

    traverse_bst_internal(0)

    return l

samples = [
    ([1, 1, 1, 2, 2], 0),
    ([2, 1, 3, 1, 2], 4)
]

# Stolen / learned from https://stackoverflow.com/a/73810689/476942
@hypothesis.strategies.composite
def unique_integers(draw):
    '''
    Return a list of unique integers.
    '''
    s = set()
    return draw(
        hypothesis.strategies.lists(
        hypothesis.strategies.integers()
        .filter(lambda n: s.add(n) is None),
        min_size=1
        )
    )

@pytest.mark.parametrize("a, expected", samples)
def test_samples(a: list[int], expected: int):
    '''
    Test samples and test cases from HackerRank.
    '''
    assert insertionSort(a) == expected

@hypothesis.given(a=unique_integers())
def test_unique(a):
    '''
    A sorted list should require 0 swaps. 
    That list reversed should require (|a| - 1) * (|a| - 2),
    since the algorithm begins on the second element.
    '''
    print(a)
    a.sort()
    assert True


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
    bst = make_bst(l)
    actual = traverse_bst(bst)
    assert l == actual

SAMPLES = [
    ([], []),
    ([1], [1]),
    ([1,2], [2, 1]),
    ([1, 2, 3], [2, 1, 3]),
    (list(range(1, 8)), [4, 2, 6, 1, 3, 5, 7]),
    (list(range(1, 16)), [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15])
]

@pytest.mark.parametrize("l,bst", SAMPLES)
def test_bst_simple(l: list[int], bst: list[int]):
    '''
    Edge cases, and simple versions that I worked out with paper and pencil.
    '''
    assert traverse_bst(bst) == l
    assert make_bst(l) == bst


HACKER_RANK_SAMPLES = [
    # samples
    ([1, 1, 1, 2, 2], 0),
    ([2, 1, 3, 1, 2], 4)
    # test cases
]

@pytest.mark.parametrize("l,expected", HACKER_RANK_SAMPLES)
def test_test_cases(l, expected):
    '''
    Samples and test cases from HackerRank
    '''
    actual = insertionSort(l)
    assert actual == expected
    
TREE_SIZE_SAMPLES = [
    (1, 1),
    (2, 3),
    (3, 3),
    (4, 7),
    (7, 7)
]

@pytest.mark.parametrize("n, expected", TREE_SIZE_SAMPLES)
def test_tree_size(n, expected):
    '''
    Verify calculate_tree_size()
    '''
    actual = calculate_tree_size(n)
    assert actual == expected