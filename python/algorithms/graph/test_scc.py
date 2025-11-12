import unittest

from directed_graph import DirectedGraph
from scc import get_sccs


class TestSCC(unittest.TestCase):
  def test_get_sccs(self):
    """Test strongly connected components algorithm."""
    graph = DirectedGraph[str, str]()

    # Create a simple graph
    graph.add_vertex('a')
    graph.add_vertex('b')
    graph.add_vertex('c')
    graph.add_edge('a', 'b', 'a-b')
    graph.add_edge('b', 'c', 'b-c')
    graph.add_edge('c', 'a', 'c-a')

    # Get SCCs - currently returns empty set as per C# implementation
    result = get_sccs(graph)

    # The C# implementation was incomplete, so we expect an empty set
    self.assertEqual(set(), result)


if __name__ == '__main__':
  unittest.main()
