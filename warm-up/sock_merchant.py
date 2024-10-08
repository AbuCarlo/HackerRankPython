'''https://www.hackerrank.com/challenges/sock-merchant/problem'''

# pylint: disable=C0103
def sockMerchant(n, ar):
    m = {}
    for sock in ar:
        m[sock] = m.get(sock, 0) + 1
    print(m)
    return sum([(count // 2) for _, count in m.items()])