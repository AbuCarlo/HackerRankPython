# https://www.hackerrank.com/challenges/min-max-riddle/problem

# "Given an integer array of size , find the maximum of the minimum(s) of every window size in the array"

import itertools

class RunByValue:
    def __init__(self, value, length):
        self.value = value
        self.length = length
        
    def __str__(self):
        return f'Run(value: {self.value}, length: {self.length})'
        

def find_runs(values):
    result = {}
    stack = [RunByValue(values[0], 1)]
    for value in values[1:]:
        # Start a new run.
        if value > stack[0].value:
            stack = [RunByValue(value, 1)] + stack
            continue
        
        pair = RunByValue(value, 1)
        length = 0
        # While the current value is less than its predecessors...
        while stack and value <= stack[0].value:
            # ...collapse this value into as many runs as you can.
            stack[0].length += length
            length = stack[0].length
            # What's the longest run with this maximum?
            result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
            stack = stack[1:]
        pair.length += length
        stack = [pair] + stack
    # The dictionary will be empty if the inputs are increasing.
    length = 0
    # If the inputs are decreasing, there will be only one run in the stack.
    while stack:
        stack[0].length += length
        length = stack[0].length
        result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
        stack = stack[1:]

    return result

def riddle(v):
    runs = find_runs(v)
    reversed = {v: k for k, v in runs.items()}
    result = []
    for i in range(1, len(v) + 1):
        # TODO We don't have a lower-bound function. Use binary search?
        result.append(reversed[i])

    r = itertools.accumulate(result, func=lambda x, y: max(x, y))
    return list(r)

sample_input = [2, 6, 1, 12]

print(riddle(sample_input))
