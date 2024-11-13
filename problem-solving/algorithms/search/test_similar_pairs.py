'''
https://www.hackerrank.com/challenges/similarpair
'''

import collections

class FenwickTree:
    '''
    https://en.wikipedia.org/wiki/Fenwick_tree

    This Fenwick tree represents the number of times
    a value occurs, not the value itself. We use it
    to count how many of node's ancestors fall
    within some range.
    '''
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        '''
        https://en.wikipedia.org/wiki/Fenwick_tree#The_update_tree
        '''
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        '''
        https://en.wikipedia.org/wiki/Fenwick_tree#The_interrogation_tree
        '''
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

# pylint: disable=C0103
def similarPair(n, k, edges):
    '''
    Use Fenwick tree to count ancestors within the
    specified range.
    '''
    tree = collections.defaultdict(list)
    for parent, child in edges:
        tree[parent].append(child)

    fenwick = FenwickTree(n)
    stack = collections.deque()
    # Pick any node to start with.
    stack.append((edges[0][0], False))
    visited = set()
    result = 0
    while stack:
        node, state = stack[-1]
        if not state:
            visited.add(node)
            left = max(1, node - k)
            right = min(n, node + k)
            # The right hand side is the "range sum."
            result += fenwick.query(right) - fenwick.query(left - 1)
            # The current node will figure in prefix sums while
            # its children are being processes.
            fenwick.update(node, 1)
            stack[-1] = (node, True)

            for child in tree[node]:
                if child not in visited:
                    stack.append((child, False))
        else:
            # Remove this node from consideration. Its children
            # have all been processed.
            fenwick.update(node, -1)
            stack.pop()
    return result

_TEST_CASE = [
    (3, 2),
    (3, 1),
    (1, 4),
    (1, 5)
]

print(similarPair(5, 2, _TEST_CASE))
