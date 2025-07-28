from typing import TypeVar
from directed_graph import DirectedGraph

TVertex = TypeVar('TVertex')
TEdge = TypeVar('TEdge')


def get_reverse(graph: DirectedGraph[TVertex, TEdge]) -> DirectedGraph[TVertex, TEdge]:
    """
    Create a reversed copy of the directed graph.

    Args:
        graph: The original directed graph

    Returns:
        A new DirectedGraph with all edges reversed
    """
    reversed_graph = DirectedGraph[TVertex, TEdge]()

    # Add all vertices first
    for vertex in graph:
        reversed_graph.add_vertex(vertex)

    # Add reversed edges - only process outgoing edges to avoid duplicates
    for vertex in graph:
        outs = graph.get_outs(vertex)

        # Reverse outgoing edges: if vertex -> target, then target -> vertex in reversed graph
        for target, edge in outs.items():
            reversed_graph.add_edge(target, vertex, edge)

    return reversed_graph
