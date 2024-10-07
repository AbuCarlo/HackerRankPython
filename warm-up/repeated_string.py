'''https://www.hackerrank.com/challenges/repeated-string/problem'''

# pylint: disable=C0103
def repeatedString(s, n):
    c = s.count('a')
    repetitions = (n // len(s))
    prefix = s[:(n % len(s))]
    return c * repetitions + prefix.count('a')