'''
https://www.hackerrank.com/challenges/subset-component/problem
'''

import pytest

# pylint: disable=C0103
def findConnectedComponents(a) -> int:
    '''
    Treat 1s in an integer as one connected component, and all 0s as singleton
    connected components. How many connected components are in the powerset
    of all the integers?
    '''
    # [] has no 1s, and therefore 64 connected components.
    result = 64
    # In how many members of the powerset of a does this 0
    # bit appear? We can include {}, which has no 1 bits!
    length_without =  1 << (len(a) - 1)
    for n in a:
        if n.bit_length() == 1:
            # A single 1 doesn't form an edge.
            result += 1
        for b in range(0, 64):
            if n & (1 << b) == 0:
                # This 0 represents a connected component in every
                # member of the powerset in which n appears.
                result += length_without

    return result


_TEST_CASES = [
    # obvious base cases
    ([3], 126),
    ([0], 128),
    ([1], 128),
    ([3, 12], 312),
    # cases from problem description
    ([2, 5, 9], 944),
    # ([1, 2, 3, 5], 504)
]

@pytest.mark.parametrize("a, expected", _TEST_CASES)
def test_test_cases(a, expected):
    '''
    Use test cases from HackerRank
    '''
    actual = findConnectedComponents(a)
    assert actual == expected
