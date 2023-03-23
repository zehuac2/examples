using System.Collections.Generic;
using Xunit;

namespace Algorithms.Graph.Tests
{
    public class DirectedGraphTest
    {
        [Fact]
        public void Test()
        {
            var graph = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "a", "b", "a-b" },
                { "b", "a", "b-a" },
            };

            Assert.Equal(new Dictionary<string, string>()
            {
                { "b", "a-b" }
            }, graph.GetOuts("a"));

            Assert.Equal(new Dictionary<string, string>()
            {
                { "a", "b-a" }
            }, graph.GetOuts("b"));

            Assert.Equal(new Dictionary<string, string>()
            {
                { "b", "b-a" }
            }, graph.GetIns("a"));

            Assert.Equal(new Dictionary<string, string>()
            {
                { "a", "a-b" }
            }, graph.GetIns("b"));
        }

        [Fact]
        public void TestEquals()
        {
            var graph = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "a", "b", "a-b" },
            };

            var expected = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "a", "b", "a-b" },
            };

            Assert.True(expected.Equals(graph));
        }

        [Fact]
        public void TestClone()
        {
            var original = new DirectedGraph<string, string>()
            {
                "a",
                "b",
                { "a", "b", "a-b" },
            };

            var cloned = original.Clone() as DirectedGraph<string, string>;
            original.Add("c");

            Assert.False(cloned.Contains("c"));
        }
    }
}
