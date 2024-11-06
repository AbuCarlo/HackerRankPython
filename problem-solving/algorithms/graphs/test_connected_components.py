'''
https://www.hackerrank.com/challenges/subset-component/problem
'''

import itertools

import pytest

# Taken directly from https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

# pylint: disable=C0103
def findConnectedComponents(a) -> int:
    '''
    Treat 1s in an integer as the edges of a connected component,
    and all 0s as singletons. How many connected components are in
    the powerset of all the integers?
    '''
    #a = [n if n.bit_count() > 1 else 0 for n in a]
    # [] has no 1s, and therefore 64 connected components.
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
    return result

_TEST_CASES = [
    ([2, 5, 9], 504),
]

@pytest.mark.parametrize("a, expected", _TEST_CASES)
def test_test_cases(a, expected):
    '''
    Use test cases from HackerRank
    '''
    actual = findConnectedComponents(a)
    assert actual == expected
