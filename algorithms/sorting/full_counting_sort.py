'''
https://www.hackerrank.com/challenges/countingsort4
'''

import io
import unittest

def count_sort_internal(a: list) -> list[str]:
    '''
    According to the examples online, this is how the 
    midpoint is calculated. The function is allowed
    to be destructive.
    '''
    midpoint = len(a) // 2
    for i in range(midpoint):
        a[i][1] = '-'
    # Python's sort() is guaranteed to be stable.
    # Destructuring doesn't work for lambda arguments.
    a.sort(key=lambda p: p[0])
    # Throw the keys away.
    return [s for _, s in a]

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
        return [[int(s[0]), s[1]] for s in [line.rstrip().split(' ') for line in reader]]

def load_output(s):
    with io.open(f'counting-sort-4/{s}', encoding='US-ASCII') as reader:
        return reader.readline()

class TestFullCountingSort(unittest.TestCase):
    '''
    Use HackerRank's test cases.
    '''
    def testTestCase(self):
        for i in [0, 1, 2, 3]:
            with self.subTest(f'Test Case {i}', i=i):
                test = load_test(f'input{i:02d}.txt')
                actual = countSortString(test)
                expected = load_output(f'output{i:02d}.txt')
                self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
