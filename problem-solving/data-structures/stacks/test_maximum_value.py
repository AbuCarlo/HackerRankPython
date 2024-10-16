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
    stack_of_stacks = collections.deque()
    result = []
    ops = [[int(s) for s in o.split(' ')] for o in operations]
    for op in ops:
        if op[0] == 1:
            n = op[1]
            if not stack_of_stacks or n > stack_of_stacks[-1][0]:
                stack = collections.deque([n])
                stack_of_stacks.append(stack)
            else:
                stack.append(op[1])
        elif op[0] == 2:
            stack_of_stacks[-1].pop()
            if not stack_of_stacks[-1]:
                stack_of_stacks.pop()
        else:
            result.append(stack_of_stacks[-1][0])
    return result

sample = ['1 97', '2', '1 20', '2', '1 26', '1 20', '2', '3', '1 91', '3']

print(getMax(sample))
