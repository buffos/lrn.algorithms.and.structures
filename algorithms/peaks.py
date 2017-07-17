"""Implement 1D and 2D Peak Finding as described in 
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/
in the first lecture.

Usage: 

p = Problem([a, b, c, ....], dims=(x,y) or None for 1D)
p.findPeak() -> (value, position)

"""

import numpy as np
import unittest


class Problem:
    def __init__(self, values, dims=None):
        if dims is None or type(dims) is not tuple or np.product(dims) != len(values):
            self.dims = (len(values),)
        else:
            self.dims = dims
        self.values = np.asarray(values).reshape(self.dims)

    def neighbors(self, position):
        if len(self.dims) == 1:
            left = max(position - 1, 0)
            right = min(position + 1, self.dims[0] - 1)
            return self.values[left], self.values[right]
        if len(self.dims) == 2:
            row, column = position[0], position[1]
            up = (max(row - 1, 0), column)
            down = (min(row + 1, self.dims[0] - 1), column)
            left = (row, max(column - 1, 0),)
            right = (row, min(column + 1, self.dims[1] - 1))
            return self.values[left], self.values[right], self.values[up], self.values[down]

    def getMax(self, column):
        """Return the index of the maximum element in the column"""
        return np.argmax(self.values[slice(None), column], axis=0)

    def isPeak(self, position):
        if len(self.dims) == 1:
            left = max(position - 1, 0)
            right = min(position + 1, self.dims[0] - 1)
            return self.values[position] >= self.values[left] and self.values[position] >= self.values[right]
        if len(self.dims) == 2:
            row, column = position[0], position[1]
            up = (max(row - 1, 0), column)
            down = (min(row + 1, self.dims[0] - 1), column)
            left = (row, max(column - 1, 0),)
            right = (row, min(column + 1, self.dims[1] - 1))
            return (self.values[position] >= self.values[left] and self.values[position] >= self.values[right] and
                    self.values[position] >= self.values[up] and self.values[position] >= self.values[down])

    def isLeftPeak(self, position):
        if len(self.dims) == 1:
            left = max(position - 1, 0)
            return self.values[position] >= self.values[left]
        if len(self.dims) == 2:
            row, column = position[0], position[1]
            left = (row, max(column - 1, 0),)
            return self.values[position] >= self.values[left]

    def isRightPeak(self, position):
        if len(self.dims) == 1:
            right = min(position + 1, self.dims[0] - 1)
            return self.values[position] >= self.values[right]
        if len(self.dims) == 2:
            row, column = position[0], position[1]
            right = (row, min(column + 1, self.dims[1] - 1))
            return self.values[position] >= self.values[right]

    def findPeak(self, start=None, end=None):
        if start is None or end is None:
            start, end = 0, self.dims[0] - 1
        mid = (end - start) // 2

        if len(self.dims) == 1:
            position = mid
        else:
            id = self.getMax(mid)  # the index ROW of the max element in the mid column
            position = id, mid

        if not self.isLeftPeak(position):
            return self.findPeak(start, mid - 1)
        elif not self.isRightPeak(position):
            return self.findPeak(mid + 1, end)
        else:  # its a peak
            return self.values[position], position


class TestProblemClass(unittest.TestCase):
    def setUp(self):
        self.v = [0, 0, 9, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 1, 0, 0, 0, 8, 9,
                  0, 2, 0, 0, 0, 0, 0,
                  0, 3, 0, 0, 0, 0, 0,
                  0, 5, 0, 0, 0, 0, 0,
                  0, 4, 7, 0, 0, 0, 0
                  ]

    def testCorrectMissingDims(self):
        self.p = Problem(self.v)
        self.assertEqual(self.p.dims, (len(self.v),),
                         "Missing dims should be completed with a tuple of the length of v")

    def testIncorrectDimsType(self):
        self.p = Problem(self.v, [2, 3])
        self.assertEqual(self.p.dims, (len(self.v),),
                         "Dims not tuple should be completed with a tuple of the length of v")

    def testIncorrectDimsDimensions(self):
        self.p = Problem(self.v, (2, 3))
        self.assertEqual(self.p.dims, (len(self.v),), "Dims should have the correct dimensions")

    def testCorrectDimsDimensions(self):
        self.p = Problem(self.v, (7, 7))
        self.assertEqual(self.p.dims, (7, 7), "Dims should be correctly stored")
        self.assertEqual(self.p.values.shape, (7, 7), "Array should be correctly reshaped")

    def testGetCorrectNeighbors2D(self):
        self.p = Problem(self.v, (7, 7))
        self.assertEqual(self.p.neighbors((3, 1)), (0, 0, 1, 3), "Should return the correct neighbors")

    def testGetCorrectNeighbors1D(self):
        self.p = Problem(self.v)
        self.assertEqual(self.p.neighbors(20), (8, 0), "Should return the correct neighbors")

    def testIsPeak1D(self):
        self.p = Problem(self.v)
        self.assertTrue(self.p.isPeak(20), "Should return position 20 as a 1D peak")

    def testIsPeak2D(self):
        self.p = Problem(self.v, (7, 7))
        self.assertTrue(self.p.isPeak((0, 2)), "Should return position 0,2 as a 2D peak")

    def testFindPeak1D(self):
        self.p = Problem(self.v)
        self.assertEqual(self.p.findPeak(), (0, 24), "Should return position 20 as a 1D peak")

    def testFindPeak2D(self):
        self.p = Problem(self.v, (7, 7))
        self.assertEqual(self.p.findPeak(), (5, (5, 1)), "Should return position 0,2 as a 2D peak")


if __name__ == '__main__':
    unittest.main()
