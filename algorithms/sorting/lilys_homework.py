'''
    https://www.hackerrank.com/challenges/lilys-homework/problem
'''

# pylint: disable=C0103
def lilysHomework(a: list[int]):
    '''Determine the minimum number of swaps to make this array "beautiful" (i.e. sorted).'''
    d = {i: n for i, n in enumerate(a)}
    pass