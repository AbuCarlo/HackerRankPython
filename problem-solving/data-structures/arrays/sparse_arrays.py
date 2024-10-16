''''
https://www.hackerrank.com/challenges/sparse-arrays/problem
'''

import collections

def matchingStrings(stringList, queries):
    counter = collections.Counter(stringList)
    return [counter[q] for q in queries]
