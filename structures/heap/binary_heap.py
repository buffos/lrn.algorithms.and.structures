""" Implementation of a Binary Heap"""
import unittest


def isRoot(i):
    return parent(i) == 0


def parent(i):
    return i // 2


def leftChild(i):
    return i * 2


def rightChild(i):
    return i * 2 + 1


class BinaryHeap:
    def __init__(self, fn=lambda parent_, child_: (parent_ < child_)):
        self.heap = ["start"]  # we skip the first position of the array for easy numbering
        self.size_ = 0
        # condition of heap for no change to happen. default is min heap
        self.fn = fn

    def __len__(self):
        """Implement the len operator"""
        return self.size_

    def __str__(self):
        return "heap: " + str(self.heap) + " size: " + str(self.size_)

    def __getitem__(self, item):
        """Can use [] notation and access Heap as an array"""
        return self.heap[item]

    def __iter__(self):
        """Implement iterator prototype for class"""
        self.current_index = 0
        return self

    def __next__(self):
        """Implement iterator prototype for class"""
        self.current_index += 1
        if self.current_index > self.size_:
            raise StopIteration
        return self.heap[self.current_index]

    def isLeaf(self, i):
        return leftChild(i) > self.size_  # it has a left child

    def isEmpty(self):
        if self.size_ == 0:
            return True
        else:
            return False

    def heapify(self, someList):
        self.size_ = len(someList)
        self.heap = ["start"]

        for element in someList:
            self.heap.append(element)

        bottomRightParent = parent(self.size_)

        while bottomRightParent > 0:  # for every non leaf node bubble down
            self.percolateDown(bottomRightParent)
            bottomRightParent -= 1

    def swapDown(self, i, j):
        """
        Swap entries between i and j position in the heap if
        heap[i] > heap[j] for a min heap
        :param :int i: ith position in heap
        :param :int j: jth position in heap
        :return :boolean : if a swap was made or not
        """
        if self.fn(self.heap[j], self.heap[i]):
            self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
            return True
        else:
            return False

    def swapUp(self, i, j):
        """
        Swap entries between i and j position in the heap if
        heap[i] < heap[j]
        :param :int i: ith position in heap
        :param :int j: jth position in heap
        :return :boolean : if a swap was made or not
        """
        if self.fn(self.heap[i], self.heap[j]):
            self.heap[j], self.heap[i] = self.heap[i], self.heap[j]
            return True
        else:
            return False

    def percolateUp(self, i):
        """
        Bubble the value at position i up until both of its children are bigger
        :param :int i: 
        :return: 
        """
        swapped = True
        while not isRoot(i) and swapped:
            swapped = self.swapUp(i, parent(i))
            i = parent(i)

    def percolateDown(self, i):
        """
        Bubble the value at position i down until both of its children are bigger
        :param :int i: 
        :return: 
        """
        swapped = True
        while not self.isLeaf(i) and swapped:
            minChild = self.minChild(i)  # get the smaller of the children
            swapped = self.swapDown(i, minChild)  # bubble i down
            i = minChild

    def insert(self, element):
        """
        Insert an element at the bottom of the heap and then let it bubble up
        :param element: 
        :return: 
        """
        self.heap.append(element)
        self.size_ += 1
        self.percolateUp(self.size_)  # entered the item at the end of the list

    def minChild(self, i):
        """
        Returns the index of the smallest of the two children of heap[i]
        :param :int i: 
        :return: 
        """
        if rightChild(i) <= self.size_:  # both children exist
            if self.fn(self.heap[rightChild(i)], self.heap[leftChild(i)]):
                # which is smaller / bigger depending on heap condition
                # the one that satisfies the heap condition better is selected
                return rightChild(i)
            else:
                return leftChild(i)
        elif leftChild(i) <= self.size_:  # the left child exists
            return leftChild(i)
        else:
            return None

    def deleteRoot(self):
        """
        Delete the root of the heap , replace it with the last element
        then decrease the size of the heap and bubble down the root to its normal position
        :return: 
        """
        rootValue = self.heap[1]
        self.heap[1] = self.heap[self.size_]  # bring the last element to the root
        self.size_ -= 1  # decrease size by one
        self.heap.pop()  # removes last element of heap
        self.percolateDown(1)  # bubble the root to the correct position
        return rootValue


class PriorityQueue(BinaryHeap):
    """It assumes that the first entry of the element in the heap is a key"""

    def __contains__(self, item):
        key = self.findKey(item)
        if key is not None:
            return True
        else:
            return False

    def findKey(self, whatToFind):
        for i in range(1, len(self.heap)):
            if self.heap[i][1] == whatToFind:
                return i
        return None

    def decreaseKey(self, whatToFind, newPriority):
        key = self.findKey(whatToFind)
        if key is not None:
            self.heap[key] = (newPriority, self.heap[key][1])
            self.percolateUp(key)  # with the new decreased key it should bubble up


class TestBinaryHeap(unittest.TestCase):
    def setUp(self):
        self.minHeap = PriorityQueue()
        self.maxHeap = PriorityQueue(fn=lambda x, y: x > y)
        self.minHeap.insert((4, 'x'))
        self.minHeap.insert((3, 'y'))
        self.minHeap.insert((5, 'z'))
        self.minHeap.insert((6, 'a'))
        self.minHeap.insert((2, 'd'))

        self.maxHeap.insert((4, 'x'))
        self.maxHeap.insert((3, 'y'))
        self.maxHeap.insert((5, 'z'))
        self.maxHeap.insert((6, 'a'))
        self.maxHeap.insert((2, 'd'))

    def testInsert(self):
        self.assertEqual(len(self.minHeap), 5, "Items in Heap are not the correct number")

    def testInsertCorrectPosition(self):
        self.minHeap.insert((1, 'x'))
        self.assertEqual(self.minHeap[1], (1, 'x'), "the element inserted did not bubble to the correct position")

    def testDeleteRoot(self):
        root = self.minHeap.deleteRoot()
        self.assertEqual(root, (2, 'd'), "the correct element was not deleted")
        self.assertEqual(len(self.minHeap), 4, "Items in Heap are not the correct number")
        self.assertEqual(self.minHeap[1], (3, 'y'), "the element inserted did not bubble to the correct position")
        self.assertEqual(self.minHeap[2], (4, 'x'), "the element inserted did not bubble to the correct position")

        root = self.maxHeap.deleteRoot()
        self.assertEqual(root, (6, 'a'), "the correct element was not deleted")
        print(self.maxHeap)
        self.assertEqual(self.maxHeap[1], (5, 'z'), "the element inserted did not bubble to the correct position")

    def testHeapify(self):
        h = [6, 5, 4, 3, 2, 1]
        self.minHeap.heapify(h)
        self.assertEqual(self.minHeap.heap, ["start", 1, 2, 4, 3, 5, 6], "the heap was not created correctly")

    def testIdentifyLeafs(self):
        self.assertTrue(self.minHeap.isLeaf(3))
        self.assertTrue(self.minHeap.isLeaf(4))
        self.assertTrue(self.minHeap.isLeaf(5))
        self.assertFalse(self.minHeap.isLeaf(2))

    def testFindKey(self):
        self.assertEqual(self.minHeap.findKey('z'), 3)

    def testDecreaseKey(self):
        self.minHeap.decreaseKey('z', 1)
        self.assertEqual(self.minHeap.findKey('z'), 1)


if __name__ == '__main__':
    unittest.main()
