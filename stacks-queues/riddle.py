# https://www.hackerrank.com/challenges/min-max-riddle/problem

# "Given an integer array of size n, find the maximum of the minimum(s) of every window size in the array"

class RunByValue:
    def __init__(self, value, length):
        self.value = value
        self.length = length

    def __repr__(self):
        return f'Run(value: {self.value}, length: {self.length})'


def find_runs(values):
    result = {}
    import collections
    stack = collections.deque([RunByValue(values[0], 1)])
    for value in values[1:]:
        # Start a new run. The current value is a new local minimum.
        if value > stack[0].value:
            stack.appendleft(RunByValue(value, 1))
            continue
        
        pair = RunByValue(value, 1)
        length = 0
        # While the current value is less than the minimum in this run...
        while stack and value <= stack[0].value:
            # ...extend the run.
            stack[0].length += length
            length = stack[0].length
            # What's the longest run with this minimum?
            result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
            stack.popleft()
        pair.length += length
        stack.appendleft(pair)
    # The dictionary will be empty if the inputs are increasing.
    length = 0
    # The stack now represents every decreasing subarray, in reverse order.
    # If the inputs are decreasing, there will be only one run in the stack.
    while stack:
        stack[0].length += length
        length = stack[0].length
        result[stack[0].value] = max(stack[0].length, result.get(stack[0].value, 0))
        stack.popleft()

    return result

def riddle(v):
    runs = find_runs(v)
    inverted = {}
    # The C++ implementation uses a tree-map.
    for k in sorted(runs.keys()):
        inverted[runs[k]] = k
    import bisect
    bisectable = sorted(inverted.keys())
    result = []
    for i in range(1, len(v) + 1):
        ix = bisect.bisect_left(bisectable, i)
        k = bisectable[ix]
        # TODO We don't have a lower-bound function. Use binary search?
        result.append(inverted[k])

    import itertools
    result = list(itertools.accumulate(reversed(result), func=lambda l,r: max(l, r)))
    result.reverse()
    return result

sample_input = [2, 6, 1, 12]

#print(riddle(sample_input))

# sample 1
# print(riddle([1, 2, 3, 5, 1, 13, 3]))

# sample 2
print(riddle([ 3, 5, 4, 7, 6, 2 ]))

# print(riddle(list(range(1, 6))))

test_case_05 = [789168277, 694294362, 532144299, 20472621, 316665904, 59654039, 685958445, 925819184, 371690486, 285650353, 522515445, 624800694, 396417773, 467681822, 964079876, 355847868, 424895284, 50621903, 728094833, 535436067, 221600465, 832169804, 641711594, 518285605, 235027997, 904664230, 223080251, 337085579, 5125280, 448775176, 831453463, 550142629, 822686012, 555190916, 911857735, 144603739, 751265137, 274554418, 450666269, 984349810, 716998518, 949717950, 313190920, 600769443, 140712186, 218387168, 416515873, 194487510, 149671312, 241556542, 575727819, 873823206]

# print(riddle(test_case_05))
