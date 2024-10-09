''''
https://www.hackerrank.com/challenges/reverse-shuffle-merge/problem
'''
import collections
import random
import unittest

# pylint: disable=C0103
def reverseShuffleMerge(s):
    '''
    :s a string after reverse-shuffle-merge. We have to reverse-engineer the source string.
    '''
    if not s:
        return ''
    counts  = collections.Counter(s)
    # An input string "A" was reversed, then a permutation of A
    # was shuffled into it to produce s. We need to get all these
    # characters into "a".
    required = {c: count // 2 for c, count in counts.items()}
    a = [s[-1]]
    required[s[-1]] -= 1
    counts[s[-1]] -= 1
    for c in reversed(s[:-1]):
        # One way or another, we're consuming this character.
        counts[s] -= 1
        # We've put as many instances of this character into "a" as necessary.
        if not required[c]:
            continue
        if c >= a[-1]:
            a.append(c)
            required[c] -= 1
            continue
        while a and c < a[-1] and counts[a[-1]] >= required[a[-1]] + 1:
            required[a.pop()] += 1
        a.append(c)
        required[c] -= 1

    return "".join(a)

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
        n = random.randint(1, 20)
        s = 'a' * (n * 2)
        self.assertEqual(reverseShuffleMerge(s), s[:n])

    def test_samples(self):
        '''samples taken from HackerRank problem description'''
        for s, expected in samples:
            self.assertEqual(reverseShuffleMerge(s), expected)

    def test_cases(self):
        '''test cases from HackerRank's "Submit"'''
        # We can use str.translate() to "reduce" the problem
        # in order to home in on the bug.
        translator = {ord(c): None for c in 'defghijk'}
        for s, expected in test_cases:
            s, expected = s.translate(translator), expected.translate(translator)
            self.assertEqual(reverseShuffleMerge(s), expected)

if __name__ == '__main__':
    unittest.main()
