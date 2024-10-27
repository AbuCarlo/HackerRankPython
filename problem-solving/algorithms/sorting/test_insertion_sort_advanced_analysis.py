'''
https://www.hackerrank.com/challenges/insertion-sort/problem
'''

import hypothesis
import hypothesis.strategies
import pytest

class _Node():
    def __init__(self, value):
        self.value = value
        # the size of any subtree.
        self.size = 1
        # the number of times a value has appeared
        self.count = 0
        # the sum of "count" for this entire subtree
        self.traversals = 0
        self.left = None
        self.right = None

    def __repr__(self):
        return f'_Node(value: {self.value}, size: {self.size}, count: {self.count}, traversals: {self.traversals})'

    def add_left_child(self, node):
        assert self.left is None
        self.left = node
        if node is not None:
            self.size += node.size

    def add_right_child(self, node):
        assert self.right is None
        self.right = node
        if node is not None:
            self.size += node.size


def create_bst(l: list[int]):
    '''
    Turn a list of integers into a binary search tree
    of all the unique values in the list.
    '''
    assert l is not None
    assert len(l) > 0

    values = list(sorted(set(l)))

    def create_bst_internal(i: int, j: int):
        assert j >= i
        if j == i:
            return None
        if j - i == 1:
            return _Node(values[i])
        midpoint = (j + i) // 2
        root = _Node(values[midpoint])
        left = create_bst_internal(i, midpoint)
        right = create_bst_internal(midpoint + 1, j)
        root.add_left_child(left)
        root.add_right_child(right)
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
    bst = create_bst(sorted(set(a)))

    swaps = 0

    for n in a:
        node = bst
        swaps_for_n = 0
        while node.value != n:
            assert node is not None
            # We know that we're adding *some* instance to this subtree.
            node.traversals += 1
            if n < node.value:
                # The subtree to the right has all values > n.
                # Include the current node in the swaps. Exclude
                # the current node (i.e. subtract the 1 we just added).
                swaps_for_n += node.traversals - 1 - node.left.traversals
                node = node.left
            else:
                node = node.right

        node.count += 1
        node.traversals += 1
        # Are there remaining values > n that would have to be traversed?
        if node.right is not None:
            swaps_for_n += node.right.traversals
        swaps += swaps_for_n

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
    # Sample Test Case 0
    ([1, 1, 1, 2, 2], 0),
    ([2, 1, 3, 1, 2], 4),
    # Sample Test Case 1
    ([12, 15, 1, 5, 6, 14, 11], 10),
    ([3, 5, 7, 11, 9], 1)
    # 
]

@pytest.mark.parametrize("l,expected", _HACKER_RANK_SAMPLES)
def test_test_cases(l, expected):
    '''
    Samples and test cases from HackerRank
    '''
    actual = insertionSort(l)
    assert actual == expected
