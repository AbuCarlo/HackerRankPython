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
    # [] has no 1s, and therefore 64 connected components.
    result = 0
    # In how many members of the powerset of a does this 0
    # bit appear? We can include {}, which has no 1 bits!
    for b in range(64):
        zeros = sum((n & (1 << b)) == 0 for n in a)
        # We've counted the values with a 0 in this position.
        # Only in the powerset of these values does this bit
        # remain a 0 (outside of that, it's ||'ed with 1).
        # Conveniently, if we count 0 0s, this bit will still
        # be a 0 in the reduction of the empty set. So "result"
        # will always be at least 1.
        result += (1 << zeros)
    singletons = list(filter(lambda n: n.bit_count() == 1, a))
    result += len(singletons)
    return result


_TEST_CASES = [
    # obvious base cases
    ([0], 128),
    ([1], 128),
    ([3], 126),
    # Only in the union of these two values is there an edge.
    ([1, 2], 254),
    # There is no edge, since all the 1s are in the same position.
    ([1, 1], 255),
    # cases from problem description
    ([1, 2, 3, 5], 944),
    ([2, 5, 9], 504),
]

@pytest.mark.parametrize("a, expected", _TEST_CASES)
def test_test_cases(a, expected):
    '''
    Use test cases from HackerRank
    '''
    actual = findConnectedComponents(a)
    assert actual == expected
