'''
https://www.hackerrank.com/challenges/countingsort4
'''

import io
import unittest

def count_sort_internal(a: list[str]) -> list[str]:
    '''
    Simply use a dictionary to bucket the strings by key.
    '''
    # pylint: disable=C0415
    from collections import defaultdict
    d = defaultdict(list)
    midpoint = len(a) // 2
    for i, (x, s) in enumerate(a):
        d[x].append((i, s if i >= midpoint else '-'))

    result = []
    for x in sorted(d.keys()):
        for i, s in d[x]:
            result.append(s)
    return result

# pylint: disable=C0103,C0116
def countSort(a: list):
    result = count_sort_internal(a)
    for i, s in enumerate(result):
        if i > 0:
            print(' ', end='')
        print(s, end='')

def countSortString(a: list[str]):
    result = count_sort_internal(a)
    return ' '.join(result)

def load_test(s):
    with io.open(f'counting-sort-4/{s}', encoding='UTF-8') as reader:
        reader.readline()
        return [(int(s[0]), s[1]) for s in [line.rstrip().split(' ') for line in reader]]


class TestFullCountingSort(unittest.TestCase):
    '''
    Use HackerRank's test cases.
    '''
    def testTestCase(self):
        test = load_test('input01.txt')
        actual = countSortString(test)
        with open('counting-sort-4/output01.txt', 'r', encoding='UTF-8') as f:
            expected = f.read().rstrip()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
