import unittest
from power_set import get_power_set

class TestPowerSet(unittest.TestCase):
    def test_power_set(self):
        expected = [
            [],
            [1],
            [2],
            [3],
            [1, 2],
            [1, 3],
            [2, 3],
            [1, 2, 3],
        ]
        set_ = [1, 2, 3]
        result = get_power_set(set_)
        # Convert all to sorted tuples for comparison
        expected_sorted = sorted([tuple(sorted(x)) for x in expected])
        result_sorted = sorted([tuple(sorted(x)) for x in result])
        for sub in result_sorted:
            self.assertIn(sub, expected_sorted)
        self.assertEqual(len(result_sorted), len(expected_sorted))

if __name__ == "__main__":
    unittest.main()
