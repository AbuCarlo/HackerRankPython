# https://www.hackerrank.com/challenges/min-max-riddle/problem

# "Given an integer array of size , find the maximum of the minimum(s) of every window size in the array"

class RunByValue:
    def __init__(self, value, length):
        self.value = value
        self.length = length
        
    def __str__(self):
        return f'Run(value: {self.value}, length: {self.length})'
        

def findRuns(values):
    result = {}
    stack = [RunByValue(values[0], 1)]
    for value in values[1:]:
        if value > stack[0].value:
            stack = [RunByValue(value, 1)] + stack
            continue
        
        pair = RunByValue(value, 1)
        length = 0
        while stack and value <= stack[0].value:
            stack[0].length += length
            length = stack[0].length
            result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
            stack = stack[1:]
        pair.length += length
        stack = [pair] + stack

    length = 0
    while stack:
        stack[0].length += length
        length = stack[0].length
        result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
        stack = stack[1:]

    return result

sample_input = [1, 2, 3, 4, 5]

print(findRuns(sample_input))
