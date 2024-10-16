'''
https://www.hackerrank.com/challenges/equal-stacks/problem
'''

from collections import deque
import heapq

# Sample Test Case 0

sample = [
    [3, 2, 1, 1, 1], [4, 3, 2], [1, 1, 4, 1]
]

def equalStacks(h1, h2, h3):
    '''
    General solution for any number of stacks of cylinders.
    '''
    # Python's heap is always a min-heap, so we have to invert the key.
    # We only compute the sums once. Compute tuples: heapify() will
    # use the first element of the tuple by default.
    stacks = [(-sum(h), deque(h)) for h in [h1, h2, h3]]
    heapq.heapify(stacks)
    # Short-circuit check that the stacks are not the same size.
    while not all(size == stacks[0][0] for size, _ in stacks[1:]):
        key, stack = stacks[0]
        # We don't have to recompute the sum; we already by
        # how much we're reducing this stack. Remember that
        # the keys are negative values.
        key += stack[0]
        stack.popleft()
        heapq.heapreplace(stacks, (key, stack))

    return -stacks[0][0]

print(equalStacks(*sample))

print(equalStacks([5], [4], [3]))
