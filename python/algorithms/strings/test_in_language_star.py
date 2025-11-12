import unittest

from in_language_star import (
  is_in_language_star_recursive,
  is_in_language_star_iterative,
)


class TestInLanguageStar(unittest.TestCase):
  def test_recursive(self):
    """Test the recursive implementation."""
    self.assertTrue(is_in_language_star_recursive('aaa', 'a'))
    self.assertFalse(is_in_language_star_recursive('aaa', 'b'))

    # Test empty string
    self.assertTrue(is_in_language_star_recursive('', 'a'))

    # Test more complex patterns
    self.assertTrue(is_in_language_star_recursive('abab', 'ab'))
    self.assertFalse(is_in_language_star_recursive('aba', 'ab'))

  def test_iterative(self):
    """Test the iterative implementation."""
    self.assertTrue(is_in_language_star_iterative('aaa', 'a'))
    self.assertFalse(is_in_language_star_iterative('aaa', 'b'))

    # Test empty string
    self.assertTrue(is_in_language_star_iterative('', 'a'))

    # Test more complex patterns
    self.assertTrue(is_in_language_star_iterative('abab', 'ab'))
    self.assertFalse(is_in_language_star_iterative('aba', 'ab'))


if __name__ == '__main__':
  unittest.main()
