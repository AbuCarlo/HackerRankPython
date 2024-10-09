''''
https://www.hackerrank.com/challenges/reverse-shuffle-merge/problem
'''
import collections
import random
import unittest

# pylint: disable=C0103
def reverseShuffleMerge(s):
    '''
    :s a string after shuffle-merge. We have to reverse-engineer the source string.
    '''
    result = ''
    counter  = collections.Counter(s)
    # An input string "A" was reversed, then a permutation was
    # shuffled into it, to produce s.
    for c in counter.keys():
        counter[c] //= 2
    shuffled = dict(counter)
    for c in reversed(s):
        # Is this the largest character we want to unload?
        if counter and c == min(counter.keys()):
            counter[c] -= 1
            result += c
        else:
            # Try to use characters from "shuffled" before 
            # larger characters from "counter".
            if shuffled[c]:
                shuffled[c] -= 1
            else:
                counter[c] -= 1
                result += c
        if counter[c] == 0:
            del counter[c]

    return result

samples = [
    ['eggegg', 'egg'],
    ['abcdefgabcdefg', 'agfedcb'],
    ['aeiouuoiea', 'aeiou']
]

# pylint: disable=C0301
test_cases = [
    [
        ('djjcddjggbiigjhfghehhbgdigjicafgjcehhfgifadihiajgciagicdahcbajjbhifjiaajigdgdfhdiijjgaiejgegbbiigida'),
        'aaaaabccigicgjihidfiejfijgidgbhhehgfhjgiibggjddjjd'
    ]
]

# pylint: disable=C0115
class TestReverseShuffleMerge(unittest.TestCase):

    def test_empty(self):
        '''The solution for an empty list is 0.'''
        self.assertEqual(reverseShuffleMerge(''), '')

    def test_single_character(self):
        '''A string of even length, repeating the same character'''
        s = 'a' * (random.randint(1, 20) * 2)
        self.assertEqual(reverseShuffleMerge(s), s[:len(s) // 2])

    def test_samples(self):
        '''samples taken from HackerRank problem description'''
        for s, expected in samples:
            self.assertEqual(reverseShuffleMerge(s), expected)

    def test_cases(self):
        '''test cases from HackerRank's "Submit"'''
        for s, expected in test_cases:
            self.assertEqual(reverseShuffleMerge(s), expected)

if __name__ == '__main__':
    unittest.main()
