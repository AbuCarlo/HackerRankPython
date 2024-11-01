'''
https://www.hackerrank.com/challenges/playing-with-numbers/problem
'''

import bisect
import itertools
import hypothesis
import hypothesis.strategies
import pytest

def absolute_element_sums(a: list[int], queries: list[int]) -> list[int]:
    '''
    Internal implementation that returns a list suitable for testing, rather
    than printing to standard output.
    '''
    a.sort()
    partial_sums = list(itertools.accumulate(a))

    # pylint: disable=C0301
    def absolute_element_sum_internal(q: int) -> int:
        if q == 0:
            # Obviously we could just sum the array! But this is a test of
            # my understanding of the boundary issues. "before_zeros" will
            # be the index of the first non-negative value, *if there is one*.
            # It will be len(a) if all values are < 0.
            before_zeros = bisect.bisect_left(a, 0)

            left_part = 0 if before_zeros == 0 else partial_sums[before_zeros - 1]
            assert left_part <= 0

            if before_zeros == len(a):
                return -left_part

            # If all values are > 0, this will == 0.
            # If all values are < 0, it will == len(a)
            after_zeros = bisect.bisect_right(a, 0)
            right_part = 0 if after_zeros == len(a) else partial_sums[-1] - partial_sums[after_zeros] + a[after_zeros]
            assert right_part >= 0

            return right_part - left_part

        if q < 0:
            before_zeros = bisect.bisect_left(a, 0)
            # Values from (∞, 0] will *decrease* by |q|, hence their absolute value will increase.
            left_part = 0 if before_zeros == 0 else partial_sums[before_zeros - 1] + before_zeros * q
            assert left_part <= 0

            if before_zeros == len(a):
                return -left_part

            # We know there are values >= 0.
            after_abs_q = bisect.bisect_right(a, -q)

            # Values from (0, |q|] will change sign. This interval is "closed" because we need to count each 0.
            middle_part = 0 if after_abs_q == before_zeros else partial_sums[after_abs_q - 1] - partial_sums[before_zeros] + a[before_zeros] + (after_abs_q - before_zeros) * q
            assert middle_part <= 0

            if after_abs_q == len(a):
                return -middle_part - left_part

            after_zeros = bisect.bisect_right(a, 0)
            # Values from [|q|, ∞) will simply decrease.
            right_part = 0 if after_zeros == len(a) else partial_sums[-1] - partial_sums[after_zeros] + a[after_zeros] + (len(a) - after_zeros) * q
            assert right_part >= 0

            return right_part - left_part - middle_part

        else:
            # If this is 0, there are *no* smaller values in the list.
            before_negative_q = bisect.bisect_left(a, -q)
            # Values from (-∞, -q] will have the same sign, but decrease in absolute value.
            left_part = 0 if before_negative_q == 0 else partial_sums[before_negative_q - 1] + (before_negative_q) * q
            assert left_part <= 0

            after_zeros = bisect.bisect_right(a, 0)
            # Values from (-q, 0] will change sign. See above comment.
            middle_part = 0 if after_zeros - before_negative_q < 1 else (partial_sums[after_zeros - 1] - partial_sums[before_negative_q] + a[before_negative_q]) + (after_zeros - before_negative_q) * q
            assert middle_part >= 0

            # Values from (0, ∞) will each increase by q.
            right_part = 0 if after_zeros == len(a) else partial_sums[-1] - partial_sums[after_zeros] + a[after_zeros] + (len(a) - after_zeros) * q
            assert right_part >= 0

            return middle_part + right_part - left_part

    results = []
    total_query = 0

    for q in queries:
        total_query += q
        result = absolute_element_sum_internal(total_query)
        results.append(result)

    return results


# pylint: disable=C0103
def playingWithNumbers(arr, queries):
    result = absolute_element_sums(arr, queries)
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
        actual = len(l) * -q - sum(l)
        assert actual == expected

    if q >= 0:
        l = [n for n in a if n <= 0 and n >= -q]
        expected = sum([abs(n - q) for n in l])
        actual = len(l) * q - sum(l)
        assert actual == expected

@hypothesis.given(hypothesis.strategies.lists(
            hypothesis.strategies.integers(min_value=-2000, max_value=2000),
            min_size=1,
            max_size=50000
        ))
def test_zero_query(l):
    '''
    Verify that we are using partial sums and binary search correctly.
    '''
    expected = sum([abs(n) for n in l])
    actual, *_ = absolute_element_sums(l, [0])
    assert actual == expected

_EDGE_CASES = [
    # my own edge cases
    ([-2, -1, 0, 0, 1, 2], 0),
    ([-2, -1, 0, 0, 1, 2], 3),
    ([-2, -1, 0, 0, 1, 2], -3),
    ([-2, -1, 0, 0, 1, 2], 1),
    ([-2, -1, 0, 0, 1, 2], -1),
]

@pytest.mark.parametrize('a,query', _EDGE_CASES)
def test_edge_cases(a, query):
    '''
    Samples from HackerRank
    '''
    expected = sum(abs(n + query) for n in a)
    actual, *_ = absolute_element_sums(a, [query])
    assert actual == expected

_TEST_CASES = [
    # problem description
    ([-1, 2, -3], [1, -2, 3], [5, 7, 6])
]

@pytest.mark.parametrize('a,queries,expected', _TEST_CASES)
def test_test_cases(a, queries, expected):
    '''
    Samples from HackerRank
    '''
    actual = absolute_element_sums(a, queries)
    assert actual == expected