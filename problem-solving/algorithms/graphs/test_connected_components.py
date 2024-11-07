'''
https://www.hackerrank.com/challenges/subset-component/problem
'''

import pytest

# pylint: disable=C0103
def findConnectedComponents(a) -> int:
    '''
    Treat 1s in an integer as the edges of a connected component,
    and all 0s as singletons. How many connected components are in
    the powerset of all the integers?
    '''
    # No singleton (power of 2) will be part of a connected component.
    # On the other hand, every other integer already forms a connected
    # component. Erase the singletons, or we'll undercount the 0s.
    a = [n if n.bit_count() > 1 else 0 for n in a]
    result = 0
    # In how many members of the powerset of a does this 0
    # bit appear? We can include {}, which has no 1 bits!
    for b in range(64):
        zeros = sum(1 for n in a if n & (1 << b) == 0)
        # We've counted the values with a 0 in this position.
        # Only in the powerset of these values does this bit
        # remain a 0 (outside of that, it's ||'ed with 1).
        # Conveniently, if we count 0 0s, this bit will still
        # be a 0 in the reduction of the empty set. So "result"
        # will always be at least 1.
        result += (1 << zeros)
    result += (1 << len(a)) - 1
    zeros = [n for n in a if n == 0]
    # However, we have now overcounted 0s,
    result -= (1 << len(zeros)) - 1
    return result

_TEST_CASES = [
    ([], 64),
    ([0], 128),
    ([1], 128),
    ([0, 0], 256),
    ([1, 0], 256),
    ([256, 0], 256),
    ([2, 5, 9], 504),
]

@pytest.mark.parametrize("a, expected", _TEST_CASES)
def test_test_cases(a, expected):
    '''
    Use test cases from HackerRank
    '''
    actual = findConnectedComponents(a)
    assert actual == expected
