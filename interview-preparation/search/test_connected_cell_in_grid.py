'''
https://www.hackerrank.com/challenges/connected-cell-in-a-grid/problem
'''

import pytest


def connectedCell(matrix):
    neighbors = {}
    neighbor = None
    for c, value in enumerate(matrix[0]):
        if value == 0:
            neighbor = None
        elif neighbor is None:
            neighbor = (0, c)
        else:
            neighbors[(0, c)] = neighbor
    for row, l in enumerate(matrix[1:]):
        


_HACKER_RANK_SAMPLES = [
    ([[1, 1, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]], 5)
]

@pytest.mark.parametrize("grid,expected", _HACKER_RANK_SAMPLES)
def test_test_cases(grid, expected):
    actual = connectedCell(grid)
    assert actual == expected