import unittest

from directed_graph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):
    def test_basic_operations(self):
        """Test basic graph operations."""
        graph = DirectedGraph[str, str]()

        # Add vertices and edges
        graph.add_vertex("a")
        graph.add_vertex("b")
        graph.add_edge("a", "b", "a-b")
        graph.add_edge("b", "a", "b-a")

        # Test outgoing edges
        expected_outs_a = {"b": "a-b"}
        self.assertEqual(expected_outs_a, graph.get_outs("a"))

        expected_outs_b = {"a": "b-a"}
        self.assertEqual(expected_outs_b, graph.get_outs("b"))

        # Test incoming edges
        expected_ins_a = {"b": "b-a"}
        self.assertEqual(expected_ins_a, graph.get_ins("a"))

        expected_ins_b = {"a": "a-b"}
        self.assertEqual(expected_ins_b, graph.get_ins("b"))

        # Test vertex count
        self.assertEqual(2, graph.vertex_count)

        # Test contains
        self.assertTrue(graph.contains("a"))
        self.assertTrue(graph.contains("b"))
        self.assertFalse(graph.contains("c"))

    def test_equals(self):
        """Test graph equality."""
        graph1 = DirectedGraph[str, str]()
        graph1.add_vertex("a")
        graph1.add_vertex("b")
        graph1.add_edge("a", "b", "a-b")

        graph2 = DirectedGraph[str, str]()
        graph2.add_vertex("a")
        graph2.add_vertex("b")
        graph2.add_edge("a", "b", "a-b")

        self.assertEqual(graph1, graph2)

    def test_clone(self):
        """Test graph cloning."""
        original = DirectedGraph[str, str]()
        original.add_vertex("a")
        original.add_vertex("b")
        original.add_edge("a", "b", "a-b")

        cloned = original.clone()
        original.add_vertex("c")

        self.assertFalse(cloned.contains("c"))
        self.assertTrue(original.contains("c"))

    def test_iteration(self):
        """Test iterating over vertices."""
        graph = DirectedGraph[str, str]()
        graph.add_vertex("a")
        graph.add_vertex("b")
        graph.add_vertex("c")

        vertices = set(graph)
        expected = {"a", "b", "c"}
        self.assertEqual(expected, vertices)


if __name__ == "__main__":
    unittest.main()
