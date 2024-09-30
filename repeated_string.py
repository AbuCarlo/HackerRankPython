def repeatedString(s, n):
    c = s.count('a')
    return c * (n // len(s)) + s[:(n % len(s))].count('a')