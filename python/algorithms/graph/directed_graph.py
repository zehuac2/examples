from typing import TypeVar, Generic, Dict, Iterator
from dataclasses import dataclass, field

TVertex = TypeVar('TVertex')
TEdge = TypeVar('TEdge')


@dataclass
class VertexData(Generic[TVertex, TEdge]):
    """Data structure to hold outgoing and incoming edges for a vertex."""
    outs: Dict[TVertex, TEdge] = field(default_factory=dict)
    ins: Dict[TVertex, TEdge] = field(default_factory=dict)


class DirectedGraph(Generic[TVertex, TEdge]):
    """A directed graph implementation with generic vertex and edge types."""

    def __init__(self):
        self._dictionary: Dict[TVertex, VertexData[TVertex, TEdge]] = {}

    @property
    def vertex_count(self) -> int:
        """Get the number of vertices in the graph."""
        return len(self._dictionary)

    def add_vertex(self, vertex: TVertex) -> None:
        """Add a vertex to the graph."""
        if vertex not in self._dictionary:
            self._dictionary[vertex] = VertexData()

    def add_edge(self, from_vertex: TVertex, to_vertex: TVertex, edge: TEdge) -> None:
        """Add an edge between two vertices."""
        if from_vertex not in self._dictionary:
            self.add_vertex(from_vertex)
        if to_vertex not in self._dictionary:
            self.add_vertex(to_vertex)

        self._dictionary[from_vertex].outs[to_vertex] = edge
        self._dictionary[to_vertex].ins[from_vertex] = edge

    def get_outs(self, vertex: TVertex) -> Dict[TVertex, TEdge]:
        """Get all outgoing edges from a vertex."""
        return self._dictionary[vertex].outs

    def get_ins(self, vertex: TVertex) -> Dict[TVertex, TEdge]:
        """Get all incoming edges to a vertex."""
        return self._dictionary[vertex].ins

    def contains(self, vertex: TVertex) -> bool:
        """Check if the graph contains a vertex."""
        return vertex in self._dictionary

    def __iter__(self) -> Iterator[TVertex]:
        """Iterate over all vertices in the graph."""
        return iter(self._dictionary.keys())

    def __eq__(self, other) -> bool:
        """Check equality with another DirectedGraph."""
        if not isinstance(other, DirectedGraph):
            return False

        if len(self._dictionary) != len(other._dictionary):
            return False

        for vertex, data in self._dictionary.items():
            if vertex not in other._dictionary:
                return False

            other_data = other._dictionary[vertex]
            if data.outs != other_data.outs or data.ins != other_data.ins:
                return False

        return True

    def clone(self) -> 'DirectedGraph[TVertex, TEdge]':
        """Create a deep copy of the graph."""
        cloned = DirectedGraph[TVertex, TEdge]()

        for vertex, data in self._dictionary.items():
            cloned._dictionary[vertex] = VertexData(
                outs=data.outs.copy(),
                ins=data.ins.copy()
            )

        return cloned
