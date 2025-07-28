import unittest
from priority_queue import PriorityQueue

class PriorityQueueTest(unittest.TestCase):
    def test_order(self):
        queue = PriorityQueue[str, int]()
        queue.add("3", 3)
        queue.add("2", 2)
        queue.add("1", 1)

        removed = queue.pop()
        self.assertEqual((1, "1"), removed)

        removed = queue.pop()
        self.assertEqual((2, "2"), removed)

        removed = queue.pop()
        self.assertEqual((3, "3"), removed)

    def test_duplicate_priorities(self):
        queue = PriorityQueue[str, int]()
        queue.add("1", 1)
        queue.add("1", 1)
        queue.add("2", 2)

        removed = queue.pop()
        self.assertEqual((1, "1"), removed)

        removed = queue.pop()
        self.assertEqual((1, "1"), removed)

        removed = queue.pop()
        self.assertEqual((2, "2"), removed)

    def test_update(self):
        queue = PriorityQueue[str, int]()
        queue.add("update", 2)
        queue.add("1", 1)

        queue.update("update", 2, 0)

        self.assertEqual((0, "update"), queue.pop())
        self.assertEqual((1, "1"), queue.pop())

if __name__ == "__main__":
    unittest.main()
