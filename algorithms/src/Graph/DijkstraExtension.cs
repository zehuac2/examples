using System.Collections.Generic;
using Algorithms.PriorityQueue;

namespace Algorithms.Graph
{
    public static class DijkstraExtension
    {
        /// <summary>
        /// Dijkstra's algorithm
        /// </summary>
        /// <typeparam name="TVertex">Type of vertex</typeparam>
        /// <typeparam name="TEdge">Type of edge</typeparam>
        /// <param name="start">Start vertex</param>
        /// <returns>
        /// The shortest distance and the prev node in shortest path of each
        /// vertex
        /// </returns>
        public static Dictionary<TVertex, (int, TVertex)> Dijkstra<TVertex, TEdge>(
            this DirectedGraph<TVertex, TEdge> graph,
            TVertex start)
            where TEdge: IVaringEdge
        {
            Dictionary<TVertex, (int, TVertex)> output = new Dictionary<TVertex, (int, TVertex)>();

            var comparer = EqualityComparer<TVertex>.Default;

            // initialize priority queue
            PriorityQueue<TVertex, int> queue = new PriorityQueue<TVertex, int>();
            queue.Add(start, 0);
            output.Add(start, (0, start));

            foreach (TVertex vertex in graph)
            {
                if (comparer.Equals(vertex, start))
                {
                    continue;
                }

                output.Add(vertex, (int.MaxValue, vertex));
                queue.Add(vertex, int.MaxValue);
            }

            // Go through all vertices
            for (int i = 0; i < graph.VertexCount; i++)
            {
                KeyValuePair<int, TVertex> peek = queue.Pop();

                foreach (KeyValuePair<TVertex, TEdge> @out in graph.GetOuts(peek.Value))
                {
                    int newLength = @out.Value.Length + peek.Key;
                    int oldLength = output[@out.Key].Item1;

                    if (newLength < oldLength)
                    {
                        output[@out.Key] = (newLength, peek.Value);
                        queue.Update(@out.Key, oldLength, newLength);
                    }
                }
            }

            return output;
        }
    }
}
