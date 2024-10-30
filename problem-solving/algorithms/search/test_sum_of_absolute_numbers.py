'''
https://www.hackerrank.com/challenges/playing-with-numbers/problem
'''

import bisect
import itertools
import hypothesis
import hypothesis.strategies
import pytest

def playing_with_numbers_internal(a: list[int], queries: list[int]) -> list[int]:
    '''
    Internal implementation that returns a list suitable for testing, rather
    than printing to standard output.
    '''
    a.sort()
    partial_sums = list(itertools.accumulate(a))
    results = []
    total_query = 0
    for q in queries:
        total_query += q
        # If q is 0, a 0 in the array won't matter (i.e. it can't affect the sum).
        # If q is < 0, each 0 in the array will get the value -q.
        # If q is > 0, each 0 will get the value q.
        before_zeros = bisect.bisect_left(a, 0)
        after_zeros = bisect.bisect_right(a, 0)

        # If q < 0, array elements < 0 remain negative. The sum of the absolute value
        # of this part of the array is simply the absolute value of the difference of the
        # partial sums at the extremes. Array elements > |q| remain positive, and their sum
        # is, again, the difference of the partial sums at the extremes. Values in [|q|, 0]
        # need special handling.
        if total_query == 0:
            left_part = partial_sums[before_zeros] - partial_sums[0]
            right_part = partial_sums[-1] - partial_sums[after_zeros]
            result = -left_part + right_part
        elif total_query < 0:
            # after_q = bisect.bisect_right(a, -q)
            left_part = partial_sums[before_zeros] - partial_sums[0]
            # If total query == 0, the sum of these values remains 0.
            # middle_part =
            right_part = partial_sums[-1] - partial_sums[after_zeros]
        else:
            before_q = bisect.bisect_left(a, -q)
            left_part = partial_sums[before_q] - partial_sums[0]

            right_part = partial_sums[-1] - partial_sums[after_zeros]
        result *= total_query
        results.append(result)
    return results


# pylint: disable=C0103
def playingWithNumbers(arr, queries):
    result = playing_with_numbers_internal(arr, queries)
    for r in result:
        print(r)


@hypothesis.strategies.composite
def array_and_query(draw):
    '''
    Return an initial array and a "query" for the HackerRank problem.
    '''
    q = draw(hypothesis.strategies.integers(min_value=-2000, max_value=2000))
    a = draw(
        hypothesis.strategies.lists(
            hypothesis.strategies.integers(min_value=-2000, max_value=2000),
            min_size=1,
            max_size=50000
        )
    )
    return (a, q)

@hypothesis.given(parameters=array_and_query())
def test_supposition(parameters):
    '''
    Validate our suppositions about the relation of q to binary searches of a.
    '''
    a, q = parameters
    if q <= 0:
        l = [n for n in a if n >= 0 and n <= -q]
        expected = sum([abs(q + n) for n in l])
        actual = len(l) * q - sum(l)
        assert actual == expected

    if q >= 0:
        l = [n for n in a if n <= 0 and n >= -q]
        expected = sum([abs(n - q) for n in l])
        actual = len(l) * q - sum(l)
        assert actual == expected

_HACKER_RANK_SAMPLES = [
    # problem description
    ([-1, 2, -3], [1, -2, 3], [5, 7, 6])
]

@pytest.mark.parametrize('a,queries,expected', _HACKER_RANK_SAMPLES)
def test_test_cases(a, queries, expected):
    '''
    Samples from HackerRank
    '''
    actual = playing_with_numbers_internal(a, queries)
    assert actual == expected
