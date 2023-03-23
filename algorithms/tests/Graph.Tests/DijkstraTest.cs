using System.Collections.Generic;
using Xunit;

namespace Algorithms.Graph.Tests
{
    public class DijkstraTest
    {
        struct Edge : IVaringEdge
        {
            public int Length { get; set; }
        }

        [Fact]
        public void Test()
        {
            var graph = new DirectedGraph<char, Edge>()
            {
                'a', 'b', 'c', 'd', 'e',
                { 'a', 'd', new Edge() { Length = 1 } },
                { 'd', 'a', new Edge() { Length = 1 } },
                { 'a', 'b', new Edge() { Length = 6 } },
                { 'b', 'a', new Edge() { Length = 6 } },
                { 'd', 'b', new Edge() { Length = 2 } },
                { 'b', 'd', new Edge() { Length = 2 } },
                { 'd', 'e', new Edge() { Length = 1 } },
                { 'e', 'd', new Edge() { Length = 1 } },
                { 'b', 'e', new Edge() { Length = 2 } },
                { 'e', 'b', new Edge() { Length = 2 } },
                { 'b', 'c', new Edge() { Length = 5 } },
                { 'c', 'b', new Edge() { Length = 5 } },
                { 'e', 'c', new Edge() { Length = 5 } },
                { 'c', 'e', new Edge() { Length = 5 } },
            };

            Dictionary<char, (int, char)> output = graph.Dijkstra('a');

            Assert.Equal((0, 'a'), output['a']);
            Assert.Equal((3, 'd'), output['b']);
            Assert.Equal((7, 'e'), output['c']);
            Assert.Equal((1, 'a'), output['d']);
            Assert.Equal((2, 'd'), output['e']);
        }
    }
}
