'''
https://www.hackerrank.com/challenges/connected-cell-in-a-grid/problem
'''

import collections

import pytest

def connectedCell(matrix):
    neighbors = {}
    for column in range(len(matrix[0]) - 1):
        if matrix[0][column] == 0:
            continue
        key = (0, column)
        if matrix[0][column + 1] == 1:
            # Point this cell at the following one.
            neighbors[key] = (0, column + 1)
        else:
            neighbors[key] = key
    for column in range(len(matrix[0]) - 2, -1, -1):
        if matrix[0][column] == 0:
            continue
        key = (0, column)
        if (0, column + 1) in neighbors:
            neighbors[key] = neighbors[(0, column + 1)]
    for row in range(1, len(matrix)):
        for column in range(0, len(matrix[row]) - 1):
            if matrix[row][column] == 0:
                continue
            key = (row, column)
            if column > 0 and matrix[row - 1][column - 1] == 1:
                neighbors[key] = neighbors[(row - 1, column - 1)]
            elif matrix[row - 1][column] == 1:
                neighbors[key] = neighbors[(row - 1, column)]
            elif column < len(matrix[row]) - 1 and matrix[row - 1][column + 1] == 1:
                neighbors[key] = neighbors[(row - 1, column + 1)]
            elif column < len(matrix[row]) - 1 and matrix[row][column + 1] == 1:
                neighbors[key] = (row, column + 1)
            else:
                neighbors[key] = key
        for column in range(len(matrix[0]) - 2, -1, -1):
            if matrix[row][column] == 0:
                continue
            if (row, column + 1) in neighbors:
                neighbors[(row, column)] = neighbors[(row, column + 1)]

    disjoint_sets = collections.defaultdict(set)
    for cell, parent in neighbors.items():
        disjoint_sets[parent].add(cell)
    sizes = [len(children) for children in disjoint_sets.values()]
    return max(sizes)

_HACKER_RANK_SAMPLES = [
    # This is the example from the text. Their answer is wrong.
    ([[1, 1, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]], 6)
]

@pytest.mark.parametrize("grid,expected", _HACKER_RANK_SAMPLES)
def test_test_cases(grid, expected):
    '''
    Samples and test cases from HackerRank
    '''
    actual = connectedCell(grid)
    assert actual == expected