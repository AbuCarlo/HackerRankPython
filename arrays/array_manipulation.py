def arrayManipulation(n, queries):
    # The problem is 1-based. In the event
    # that a "query" extends all the way to
    # the end of the array, we'll need to put
    # the summand in a final, extra element.
    a = [0] * (n + 2)
    for l, j, summand in queries:
        a[l] += summand
        a[j + 1] -= summand
        
    import itertools
    # Now trim the array again.
    b = itertools.accumulate(a[1:-1])
    return max(b)

sample00 = [[1, 5, 3], [4, 8, 7], [6, 9, 1]]

print(arrayManipulation(10, sample00))