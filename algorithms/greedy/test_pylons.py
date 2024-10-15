'''
https://www.hackerrank.com/challenges/pylons/problem

Prepare | Algorithms | Greedy | Goodland Electricity
'''
import sys

import hypothesis
import hypothesis.statistics
import hypothesis.strategies

d = {}

def pylons_internal(i: int, j: int, k: int, a: list[int]) -> int:
    # a[i] contains a pylon. How many 0s are there until
    # the next pylon?
    while j < len(a) and a[j] == 0:
        j += 1
    # Are we at the end of a? If so, how many 0s followed the last pylon?
    if j == len(a):
        return None if j - i > k else 0
    # We found another pylon. Is it too far from a[i]?
    if j - i > 2 * k - 1:
        return None
    key = (i, j)
    if key in d:
        return d[key]
    yes = pylons_internal(j, j + 1, k, a)
    # If we place a pylon here, and still have no
    # solution, there's no point in proceeding.
    # Obviously we'd leave an even longer interval
    # of unelectrified cities if we didn't place a
    # pylon here.
    if yes is None:
        return None
    # What's the optimal solution if we *don't* put a pylon here?
    no = pylons_internal(i, j + 1, k, a)
    solution = None
    if no is None:
        solution = 1 + yes
    elif no <= yes:
        solution = no
    else:
        solution = 1 + yes
    d[key] = solution
    return solution

def pylons(k: int, a: list[int]) -> int:
    '''
    How many pylons do we to place in order for every city to have electricity?
    
    :param k: a city must be at a distance < k from a pylon
    :param a: a list of cities, 1 denoting pylon-readiness
    :return: the optimal solution or -1 if no solution is possible
    '''
    solutions = []
    memos = {}
    starts = []

    # Populate the stack with possible solutions starting with any 1 value in a[0:k].
    for i, e in enumerate(a):
        if i >= k:
            break
        if e == 0:
            continue
        key = (i, i + 1)
        starts.append(key)
        # s = pylons_internal(i, i + 1, k, a)
        # if s is not None:
        #     solution = min(s + 1, solution)
    for start in starts:
        # pylint: disable=C0415
        import collections
        stack = collections.deque()
        stack.append(start)
        while stack:
            key = stack[-1]
            if key in memos:
                stack.pop()
                continue
            i, j = key
            assert a[i] == 1
            # a[i] contains a pylon. How many 0s are there until the next pylon?
            jj = j
            while jj < len(a) and a[jj] == 0:
                jj += 1
            # Are we at the end of a? If so, how many 0s followed the last pylon?
            if jj == len(a):
                solution = None if jj - i > k else 0
                memos[key] = solution
                continue
            # We found another pylon. Is it too far from a[i]?
            if jj - i > 2 * k - 1:
                return None

            
            
        solutions.append(memos[start])
            
            

        
        
        
        
        
        
    return solution if solution < sys.maxsize else -1


# pytest .\algorithms\greedy\pylons.py

def test_samples():
    '''samples from HackerRank"'''
    # "Example" from problem description
    assert(pylons(3, [0, 1, 1, 1, 0, 0, 0])) == -1
    # "Sample"
    assert pylons(2, [0, 1, 1, 1, 1, 0]) == 2
    # samples test cases from "Run Code"
    assert pylons(2, [0, 1, 1, 1, 1, 0]) == 2
    assert pylons(2, [0, 1, 0, 0, 0, 1, 0]) == -1
    assert pylons(3, [0, 1, 0, 0, 0, 1, 1, 1, 1, 1]) == 3


def test_test_cases():
    '''Run test cases from dowloaded input files'''
    for t, expected in [(4, 28), (12, 1206), (16, 6864)]:
        path = f'algorithms/greedy/pylons-inputs/input{t:02d}.txt'
        with open(path, 'r', encoding='UTF-8') as f:
            _, k = f.readline().rstrip().split(' ')
            a = [int(s) for s in f.readline().rstrip().split(' ')]
            assert pylons(int(k), a) == expected

# pylint: disable=C0415
def test_performance():
    '''Test performance to achieve full score.'''
    import functools
    def benchmark(k, a):
        pylons(k, a)

    executions = 100
    with open('algorithms/greedy/pylons-inputs/input04.txt', 'r', encoding='UTF-8') as f:
        _, k = f.readline().rstrip().split(' ')
        a = [int(s) for s in f.readline().rstrip().split(' ')]
        p = functools.partial(benchmark, int(k), a)
        from timeit import timeit
        perf = timeit(p, number=executions) / executions
        assert perf < .001
        # pytest will suppress this output.
        print(f'File {p} took avg. time={perf} ms')


# @hypothesis.given(
#     hypothesis.strategies.lists(hypothesis.strategies.booleans(), min_size=1, max_size=100)
# )
# def test_zero_pylons(a):
#     '''0 pylons will not suffice for any number of cities.'''
#     cities = [1 if b else 0 for b in a]
#     assert pylons(0, cities) == -1

# @hypothesis.given(
#     hypothesis.strategies.integers(min_value=1, max_value=100)
# )
# def test_electrify_every_city(n):
#     '''If there are as many pylons as cities, there is a solution.'''
#     cities = [1] * n
#     assert pylons(n, cities) > 0

