'''
https://www.hackerrank.com/challenges/maximum-element/problem
'''

import collections

# pylint: disable=C0103
def getMax(operations: list[str]) -> list[int]:
    '''
    At any point, provide the maximum value contained in the stack.
    This is a tiresome interview classic. I propose to implement it
    as a stack of stacks. In C++, I'd have to maintain a stack of
    maxima-per-stack, and pop or push whenever I pop or push a stack.
    In Python I can cheat, since a stack is just a deque: the maximum
    for a stack is element 0.
    
    :param operations: a list of operations
    
    1 x  -Push the element x into the stack.
    2    -Delete the element present at the top of the stack.
    3    -Print the maximum element in the stack.
    '''
    maxima = collections.deque()
    counts = collections.deque()
    result = []
    ops = [[int(s) for s in o.split(' ')] for o in operations]
    for op in ops:
        if op[0] == 1:
            n = op[1]
            if not maxima or n > maxima[-1]:
                maxima.append(n)
                counts.append(1)
            else:
                counts[-1] += 1
        elif op[0] == 2:
            assert counts
            counts[-1] -= 1
            if counts[-1] == 0:
                counts.pop()
                maxima.pop()
        else:
            result.append(maxima[-1])
    return result

sample = ['1 97', '2', '1 20', '2', '1 26', '1 20', '2', '3', '1 91', '3']

print(getMax(sample)) # [26, 91]

# DOWNLOADS = 'problem-solving/data-structures/stacks/get-max-value-inputs'
DOWNLOADS = './get-max-value-inputs'


# pylint: disable=C0116
def load(i):
    path = f'{DOWNLOADS}/input{i:02d}.txt'
    with open(path, 'r', encoding='UTF-8') as f:
        size = int(f.readline().rstrip())
        operations = f.readlines()
        assert len(operations) == size
        return operations

problem = load(4)
actual = getMax(problem)
print(actual)
