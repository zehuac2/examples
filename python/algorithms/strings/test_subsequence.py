import unittest

from subsequence import longest_increasing_subsequence_recursive


class TestSubsequence(unittest.TestCase):
    def test_longest_increasing_subsequence_recursive(self):
        """Test the recursive longest increasing subsequence implementation."""
        # Test case 1: [int.MinValue, 1, 2, 3] should return 3
        values1 = [-2147483648, 1, 2, 3]  # int.MinValue in Python
        self.assertEqual(3, longest_increasing_subsequence_recursive(values1))

        # Test case 2: [int.MinValue, 2, 3, 3, 2, 4, 5] should return 4
        values2 = [-2147483648, 2, 3, 3, 2, 4, 5]
        self.assertEqual(4, longest_increasing_subsequence_recursive(values2))

        # Test empty list
        self.assertEqual(0, longest_increasing_subsequence_recursive([]))

        # Test single element
        self.assertEqual(1, longest_increasing_subsequence_recursive([1]))


if __name__ == "__main__":
    unittest.main()
