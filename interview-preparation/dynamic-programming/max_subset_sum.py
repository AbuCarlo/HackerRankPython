'''https://www.hackerrank.com/challenges/max-array-sum/problem'''

import itertools
import random
import unittest

import hypothesis
import parameterized

# pip install parameterized

# pylint: disable=C0103
def maxSubsetSum(a):
    '''Given an array of integers, find the subset of non-adjacent
    elements with the maximum sum.'''
    far = 0
    near = 0
    for n in a:
        if n <= 0:
            far = max(far, near)
        else:
            # "far" is now far, so we can assign it
            # to "near". We can bump "near".
            near, far =  (far + n, max(far, near))
    return max(far, near)

def powerset(iterable):
    ''' See https://docs.python.org/2/library/itertools.html#recipes'''
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def non_adjacent(upper):
    '''Generate all subsets such that no two adjacent elements will be selected.'''
    sets = powerset(range(upper))
    # itertools.pairwise() added in 3.10; HackerRank is lagging.
    # Eliminate combinations with consecutive indices.
    return filter(lambda l: all(p[1] - p[0] > 1 for p in itertools.pairwise(l)), sets)

class TestStringMethods(unittest.TestCase):
    '''Unit tests for non_adjacent()'''
    Limit = 20

    def test_empty(self):
        '''The solution for an empty list is 0.'''
        self.assertEqual(maxSubsetSum([]), 0)

    @hypothesis.given(
        hypothesis.strategies.lists(
            hypothesis.strategies.integers(min_value=-20, max_value=-1),
            max_size=10))
    def test_negatives(self, negatives):
        '''If all values are <= 0, the solution is 0.'''    
        self.assertEqual(maxSubsetSum(negatives), 0)

    # TODO Use Hypothesis.
    def test_sorted(self):
        '''For a sorted array of positive numbers, the solution will include the final (largest) value.'''
        srted =  sorted([random.randint(1, 1000) for _ in range(TestStringMethods.Limit)])
        expected = sum(srted[i] for i in range(20) if i % 2 == 1)
        self.assertEqual(maxSubsetSum(srted), expected)

    @parameterized.parameterized.expand([
        ([3, 7, 4, 6, 5], 13),
        ([2, 1, 5, 8, 4], 11),
        ([3, 5, -7, 8, 10], 15)
    ])
    def test_samples(self, a, expected):
        '''Samples taken from HackerRank'''
        self.assertEqual(maxSubsetSum(a), expected)

    def test_mixed(self):
        '''For all other inputs, generate all possible combinations of non-adjacent elements
        Then find the maximum sum among them.'''
        mixed = [random.randint(-1000, 1000) for _ in range(TestStringMethods.Limit)]
        possible_indices = non_adjacent(TestStringMethods.Limit)
        possible_subarrays = [[mixed[i] for i in pi] for pi in possible_indices]
        expected = max(sum(p) for p in possible_subarrays)
        self.assertEqual(maxSubsetSum(mixed), expected)

if __name__ == '__main__':
    unittest.main()
