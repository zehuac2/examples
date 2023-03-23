using System.Collections.Generic;

namespace Algorithms.Graph
{
    public static class SCCExtension
    {
        public static HashSet<HashSet<V>> GetSCCs<V, E>(
            this DirectedGraph<V, E> graph)
        {
            DirectedGraph<V, E> reversed = graph.GetReverse();
            var copyGraph = graph.Clone() as DirectedGraph<V, E>;

            return new HashSet<HashSet<V>>();
        }
    }
}
