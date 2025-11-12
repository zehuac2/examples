import unittest

from directed_graph import DirectedGraph
from dijkstra import dijkstra
from varying_edge import VaryingEdge


class Edge(VaryingEdge):
  """Simple edge implementation for testing."""

  def __init__(self, length: int):
    self._length = length

  @property
  def length(self) -> int:
    return self._length


class TestDijkstra(unittest.TestCase):
  def test_dijkstra(self):
    """Test Dijkstra's algorithm."""
    graph = DirectedGraph[str, Edge]()

    # Add vertices
    vertices = ['a', 'b', 'c', 'd', 'e']
    for vertex in vertices:
      graph.add_vertex(vertex)

    # Add edges as per the C# test
    graph.add_edge('a', 'd', Edge(1))
    graph.add_edge('d', 'a', Edge(1))
    graph.add_edge('a', 'b', Edge(6))
    graph.add_edge('b', 'a', Edge(6))
    graph.add_edge('d', 'b', Edge(2))
    graph.add_edge('b', 'd', Edge(2))
    graph.add_edge('d', 'e', Edge(1))
    graph.add_edge('e', 'd', Edge(1))
    graph.add_edge('b', 'e', Edge(2))
    graph.add_edge('e', 'b', Edge(2))
    graph.add_edge('b', 'c', Edge(5))
    graph.add_edge('c', 'b', Edge(5))
    graph.add_edge('e', 'c', Edge(5))
    graph.add_edge('c', 'e', Edge(5))

    # Run Dijkstra from 'a'
    result = dijkstra(graph, 'a')

    # Verify results
    self.assertEqual((0, 'a'), result['a'])
    self.assertEqual((3, 'd'), result['b'])
    self.assertEqual((7, 'e'), result['c'])
    self.assertEqual((1, 'a'), result['d'])
    self.assertEqual((2, 'd'), result['e'])


if __name__ == '__main__':
  unittest.main()
