using Xunit;

namespace Algorithms.Graph.Tests
{
    public class ReverseTest
    {
        [Fact]
        public void Test()
        {
            var graph = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "a", "b", "edge" },
            };

            var reversedGraph = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "b", "a", "edge" },
            };

            Assert.Equal(reversedGraph, graph.GetReverse());
        }
    }
}
