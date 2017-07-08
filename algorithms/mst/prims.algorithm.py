"""
From 'Wikipedia' (https://en.wikipedia.org/wiki/Prim%27s_algorithm)

  In computer science, Prim's algorithm is a greedy algorithm that finds
a minimum spanning tree for a weighted undirected graph.

  This means it finds a subset of the edges that forms a tree that includes every vertex,
where the total weight of all the edges in the tree is minimized. The algorithm operates
by building this tree one vertex at a time, from an arbitrary starting vertex, at each step
adding the cheapest possible connection from the tree to another vertex.

* Algorithm pseudocode
  - Initialize a tree with a single vertex, chosen arbitrarily from the graph.
  - Grow the tree by one edge: of the edges that connect the tree to vertices not yet in the tree, find the minimum-weight edge, and transfer it to the tree.
  - Repeat step 2 (until all vertices are in the tree).
"""

from context import structures
import sys

import unittest
from structures.heap.binary_heap import PriorityQueue


def prim(graph, start, distance):
    # start is a vertex in graph
    h = [(distance(start, vertex), vertex) for vertex in graph]
    pq = PriorityQueue()
    pq.heapify(h)

    while not pq.isEmpty():
        # the first popped root would be start
        u = pq.deleteRoot()[1]
        for v in u.connections():
            d = distance(u, v)
            pq.decreaseKey(v, d) # decrease distance if its lower and v in pq


class TestPrimsAlgorithm(unittest.TestCase):
    def testDummy(self):
        pass

if __name__ == '__main__':
    unittest.main()
