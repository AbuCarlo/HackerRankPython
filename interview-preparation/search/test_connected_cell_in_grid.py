'''
https://www.hackerrank.com/challenges/connected-cell-in-a-grid/problem
'''

import collections

import pytest

# pylint: disable=C0103
def connectedCell(matrix):
    '''
    Solution implemented as directed graph, from which disjoint sets
    were created. The size of the largest disjoint set is the answer.
    '''
    adjacency = collections.defaultdict(set)
    for column in range(len(matrix[0])):
        if matrix[0][column] == 0:
            continue
        key = (0, column)
        adjacency[key].add(key)
        if column < len(matrix[0]) - 1 and matrix[0][column + 1] == 1:
            # Point this cell at the following one.
            adjacency[key].add((0, column + 1))
    for row in range(1, len(matrix)):
        for column in range(0, len(matrix[row])):
            if matrix[row][column] == 0:
                continue
            key = (row, column)
            adjacency[key].add(key)
            if column > 0 and matrix[row - 1][column - 1] == 1:
                adjacency[key].add((row - 1, column - 1))
            if matrix[row - 1][column] == 1:
                adjacency[key].add((row - 1, column))
            if column < len(matrix[row]) - 1 and matrix[row - 1][column + 1] == 1:
                adjacency[key].add((row - 1, column + 1))
            if column < len(matrix[row]) - 1 and matrix[row][column + 1] == 1:
                adjacency[key].add((row, column + 1))

    # Conveniently, we can count the 1s this way.
    adjacency_size = sum([sum(row) for row in matrix])
    assert len(adjacency) == adjacency_size

    parents = {}
    disjoint_sets = collections.defaultdict(set)

    for cell in adjacency:
        parents[cell] = cell
        disjoint_sets[cell] = set([cell])

    def _find_root(cell):
        parent = parents[cell]
        while parent != parents[parent]:
            parent, parents[parent] = parents[parent], parents[parents[parent]]
        return parent

    for cell, neighbors in adjacency.items():
        for neighbor in neighbors:
            x = _find_root(cell)
            y = _find_root(neighbor)
            if x == y:
                continue

            parents[y] = x
            disjoint_sets[x] |= disjoint_sets[y]
            disjoint_sets.pop(y)

    sizes = [len(children) for children in disjoint_sets.values()]
    return max(sizes)


_HACKER_RANK_SAMPLES = [
    # This is the example from the text. Their answer is wrong.
    ([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]], 5),
    # Sample Test Case 2
    ([[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 0, 1, 1]], 5),
    # Test Case 1
    ([[0, 0, 1, 1], [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]], 8),
    # Test Case 6
    ([
        [0, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1],
        [0, 1, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 0]
    ], 29)
]

@pytest.mark.parametrize("grid,expected", _HACKER_RANK_SAMPLES)
def test_test_cases(grid, expected):
    '''
    Samples and test cases from HackerRank
    '''
    actual = connectedCell(grid)
    assert actual == expected
