from typing import TypeVar, Dict, Tuple
from .directed_graph import DirectedGraph
from .varying_edge import VaryingEdge

TVertex = TypeVar('TVertex')
TEdge = TypeVar('TEdge', bound=VaryingEdge)

# Use a large value instead of infinity for compatibility with int type
MAX_INT = 2**31 - 1


def dijkstra(graph: DirectedGraph[TVertex, TEdge], start: TVertex) -> Dict[TVertex, Tuple[int, TVertex]]:
    """
    Dijkstra's algorithm for finding shortest paths.

    Args:
        graph: The directed graph to search
        start: The starting vertex

    Returns:
        Dictionary mapping each vertex to (shortest_distance, previous_vertex)
    """
    # Import here to avoid circular imports if needed
    from priority_queue import PriorityQueue

    output: Dict[TVertex, Tuple[int, TVertex]] = {}

    # Initialize priority queue
    queue = PriorityQueue[TVertex, int]()
    queue.add(start, 0)
    output[start] = (0, start)

    # Initialize all other vertices with max distance
    for vertex in graph:
        if vertex == start:
            continue
        output[vertex] = (MAX_INT, vertex)
        queue.add(vertex, MAX_INT)

    # Process all vertices
    for _ in range(graph.vertex_count):
        if queue.count == 0:
            break

        distance, current_vertex = queue.pop()

        # Check all outgoing edges from current vertex
        for neighbor, edge in graph.get_outs(current_vertex).items():
            new_distance = edge.length + distance
            old_distance = output[neighbor][0]

            if new_distance < old_distance:
                output[neighbor] = (new_distance, current_vertex)
                queue.update(neighbor, old_distance, new_distance)

    return output
