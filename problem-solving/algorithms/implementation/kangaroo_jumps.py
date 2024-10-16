'''
https://www.hackerrank.com/challenges/kangaroo/problem
'''

def kangaroo(x1, v1, x2, v2):
    # Assume x2 > x1.
    if v2 >= v1:
        # The trailing kangaroo can never catch up.
        return 'NO'
    # If the difference in starting points is evenly
    # divisible by the difference in jumps, then 
    # the kangaroos can reach the same square.
    # The corresponding integer division would give
    # use the required numbr of jumps.
    return 'YES' if (x2 - x1) % (v1 - v2) == 0 else 'NO'
