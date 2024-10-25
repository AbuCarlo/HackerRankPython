'''
https://www.hackerrank.com/challenges/insertion-sort/problem
'''

import hypothesis
import hypothesis.strategies
import pytest

# Let's invent a data structure: (n, count, total_count)
# total_count will be the sum of the total_count fields
# of the two children + the sum of each child's count.

def check_heap_invariant(h: list, i: int):
    left, right = 2 * i + 1, 2 * i + 2
    actual = 0
    if left < len(h) and h[left] is not None:
        actual += h[left][1] + h[left][2]
    if right < len(h) and h[right] is not None:
        actual += h[right][1] + h[left][2]
    assert actual == h[i][2]

def heap_find(h: list, n: int):
    result = 0
    i = 0
    odd = (n % 2) == 1
    while True:
        # The value is not in the heap yet.
        if i >= len(h) or h[i] is None or n > h[i][0]:
            return None
        check_heap_invariant(h, i)
        if h[i][0] == n:
            # The value is in the heap
            _, previous_count, previous_total_count = h[i]
            h[i] = (n, previous_count + 1, previous_total_count)
            return result
        else:
            result += h[i][2]
            sub_x, sub_y = 2 * i + 1, 2 * i + 2
            result += h[i][1]
            if not odd:
                sub_x, sub_y = sub_y, sub_x
            i = sub_x
            if sub_y < len(h) and h[sub_y] is not None:
                result -= h[sub_y][2]


def heap_insert(h: list, n: int):
    '''
    Count the number of elements > n, leftward of n:
    this is the number of swaps before n reaches its
    correct position on this iteration.
    '''
    found = heap_find(h, n)
    if found is not None:
        return found

    result = 0
    i = 0
    while True:
        if i >= len(h):
            # 0, 1, 3, 7, 15, ...
            h.extend([None] * (len(h) + 1))
        # We've never encountered n.
        if h[i] is None:
            # Implement the swap algorithm.
            h[i] = (n, 1, 0)
            return result
        elif h[i][1] == n:
            _, previous_count, previous_total_count = h[i]
            h[i] = (n, previous_count + 1, previous_total_count)
            return result
        else:
            # Add the current element as 1, plus
            # the sum of the sizes of its two subtrees.
            result += h[i][2] + 1
            # The two subtrees of h[i]
            subtree, other = 2 * i + 1, 2 * i + 2
            assert h[i][2] == h[subtree][2] + h[other][2]
            if n % 2 == 0:
                subtree, other = other, subtree
            # Subtract the size of the subtree we're *not* following.
            result -= h[other][2]
            i = subtree

# pylint: disable=C0103
def insertionSort(a):
    '''
    Count the number of swaps that an insertion sort on this 
    array would require.
    
    :param a: an unsorted array to be sorted
    :returns: the number of swaps
    '''
    h = []
    swaps = 0
    for i in range(1, len(a)):
        swaps += heap_insert(h, a[i])
    return swaps

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


def make_bst(l: list[int]):
    if not l:
        return []
    # A perfectly balanced tree will have a
    # size 2^n - 1 for some n. We want to round
    # len() up to a power of 2, unless it's
    # already a power of 2, in which case
    # we need to round it up one more time.
    size = (1 << (len(l) + 1).bit_length() - 1) - 1
    root = size // 2
    width = (size + 1) // 2
    bst = [0] * len(l)
    bst[0] = l[root]
    i = 0
    while width > 1:
        for j in range((width // 2) - 1, len(l), width):
            # This happens on the first iteration.
            if j == root:
                continue
            bst[i + 1] = l[j]
            i += 1
        width //= 2
    return bst


def traverse_bst_internal(bst: list[int], i: int, l: list[int]):
    if i >= len(bst):
        return
    traverse_bst_internal(bst, 2 * i + 1, l)
    l.append(bst[i])
    traverse_bst_internal(bst, 2 * i + 2, l)


def traverse_bst(bst: list[int]):
    if not bst:
        return []
    l = []
    traverse_bst_internal(bst, 0, l)
    return l

@hypothesis.given(hypothesis.strategies.lists(hypothesis.strategies.integers(min_value=1, max_value=10000000), min_size=1, max_size=100000))
def test_bst_round_trip(l: list[int]):
    '''
    Verify that an BST represents the original array by 
    depth-first traversal. The limits above are from the 
    original problem.
    '''
    l.sort()
    bst = make_bst(l)
    actual = traverse_bst(bst)
    assert l == actual

SAMPLES = [
    ([], []),
    ([1], [1]),
    ([1, 2, 3], [2, 1, 3]),
    (list(range(1, 8)), [4, 2, 6, 1, 3, 5, 7]),
    (list(range(1, 16)), [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15])
]

@pytest.mark.parametrize("l,bst", SAMPLES)

def test_bst_simple(l: list[int], bst: list[int]):
    # Edge cases, and simple versions that I worked out with paper and pencil.
    assert traverse_bst(bst) == l
    assert make_bst(l) == bst
