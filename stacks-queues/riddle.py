class Run:
    def __init__(self, value, length):
        self.value = value
        self.length = length
        
    def __str__(self):
        return f'Run(value: {self.value}, length: {self.length})'
        

def findRuns(values):
    result = {}
    stack = [[values[0], 1]]
    for value in values[1:]:
        if value > stack[0][0]:
            stack = [[value, 1]] + stack
            continue
        
        pair = [value, 1]
        length = 0
        while stack and value <= stack[0][0]:
            stack[0][1] += length
            length = stack[0][1]
            result[stack[0][0]] = max(stack[0][1], result.get(stack[0][0], 0))
            stack = stack[1:]
        pair[1] += length
        stack = [pair] + stack
        
    length = 0
    while stack:
        stack[0][1] += length
        length = stack[0][1]
        result[stack[0][0]] = max(stack[0][1], result.get(stack[0][0], 0))
        stack = stack[1:]

    return result

sample_input = [5, 4, 3, 2, 1]

print(findRuns(sample_input))

print(Run(0, 1))