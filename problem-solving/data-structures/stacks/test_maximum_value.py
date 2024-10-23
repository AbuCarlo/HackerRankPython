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

def test_sample():
    '''
    For pytest. The problem only comes with one sample.
    '''
    sample = ['1 97', '2', '1 20', '2', '1 26', '1 20', '2', '3', '1 91', '3']
    actual = getMax(sample)
    assert actual == [26, 91]

DOWNLOADS = 'problem-solving/data-structures/stacks/get-max-value-inputs'

def load(i):
    '''
    Load matching input and output files downloaded 
    from the HackerRank problem page.
    
    :param i: the number of the problem
    
    :return: a tuple of the input values and expected output
    '''
    input_path = f'{DOWNLOADS}/input{i:02d}.txt'
    with open(input_path, 'r', encoding='UTF-8') as f:
        size = int(f.readline().rstrip())
        operations = f.readlines()
        assert len(operations) == size
    output_path = f'{DOWNLOADS}/output{i:02d}.txt'
    with open(output_path, 'r', encoding='UTF-8') as f:
        maxima = [int(l) for l in f.readlines()]
    return (operations, maxima)

def test_test_case(benchmark):
    '''
    Benchmark HackerRank's test cases for full score.
    '''
    operations, expected = load(4)
    actual = benchmark(getMax, operations)
    assert actual == expected
