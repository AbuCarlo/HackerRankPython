'''

'''

# Sample Test Case 0

sample = [
    [3, 2, 1, 1, 1], [4, 3, 2], [1, 1, 4, 1]
]

def equalStacks(h1, h2, h3):
    '''
    '''
    # pylint: disable=C0415
    from collections import deque
    stacks = [deque(h) for h in [h1, h2, h3]]
    while not all(sum(s) == sum(stacks[0]) for s in stacks[1:]):
        largest = max(stacks, key=sum)
        largest.popleft()

    return sum(stacks[0])
    
print(equalStacks(*sample))