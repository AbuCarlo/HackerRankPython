'''
https://www.hackerrank.com/challenges/crush/problem

"Starting with a 1-indexed array of zeros and a list of operations,
for each operation add a value to each the array element between two given indices, inclusive.
Once all operations have been performed, return the maximum value in the array.
"

'''

import itertools

# pylint: disable=C0103,C0116
def arrayManipulation(n, queries):
    # The problem is 1-based. In the event
    # that a "query" extends all the way to
    # the end of the array, we'll need to put
    # the summand in a final, extra element.
    a = [0] * (n + 2)
    for l, j, summand in queries:
        a[l] += summand
        a[j + 1] -= summand

    # Now trim the array again.
    b = itertools.accumulate(a[1:-1])
    return max(b)

sample00 = [[1, 5, 3], [4, 8, 7], [6, 9, 1]]

assert arrayManipulation(10, sample00) == 10
