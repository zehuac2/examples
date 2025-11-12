import unittest

from directed_graph import DirectedGraph
from reverse import get_reverse


class TestReverse(unittest.TestCase):
  def test_get_reverse(self):
    """Test graph reversal."""
    original = DirectedGraph[str, str]()

    # Create a simple graph: a -> b, b -> c
    original.add_vertex('a')
    original.add_vertex('b')
    original.add_vertex('c')
    original.add_edge('a', 'b', 'a-b')
    original.add_edge('b', 'c', 'b-c')

    # Get reversed graph
    reversed_graph = get_reverse(original)

    # In reversed graph: b -> a, c -> b
    self.assertEqual({'a': 'a-b'}, reversed_graph.get_outs('b'))
    self.assertEqual({'b': 'b-c'}, reversed_graph.get_outs('c'))
    self.assertEqual({}, reversed_graph.get_outs('a'))

    # Check incoming edges
    self.assertEqual({'b': 'a-b'}, reversed_graph.get_ins('a'))
    self.assertEqual({'c': 'b-c'}, reversed_graph.get_ins('b'))
    self.assertEqual({}, reversed_graph.get_ins('c'))

    # Verify all vertices are present
    self.assertTrue(reversed_graph.contains('a'))
    self.assertTrue(reversed_graph.contains('b'))
    self.assertTrue(reversed_graph.contains('c'))


if __name__ == '__main__':
  unittest.main()
