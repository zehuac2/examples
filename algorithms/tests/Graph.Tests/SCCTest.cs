using System.Collections.Generic;
using Xunit;

namespace Algorithms.Graph.Tests
{
    public class SCCTest
    {
        [Fact]
        public void TestSCCs()
        {
            var graph = new DirectedGraph<string, string>()
            {
                "A", "B", "C", "D", "E", "F", "G", "H",
                { "B", "E", "B-E" },
                { "A", "B", "A-B" },
                { "A", "F", "A-F" },
                { "A", "C", "A-C" },
                { "C", "D", "C-D" },
                { "D", "A", "D-A" },
                { "D", "H", "D-H" },
                { "H", "G", "H-G" },
                { "F", "B", "F-B" },
                { "F", "G", "F-G" },
                { "E", "F", "E-F" },
                { "E", "G", "E-G" },
                { "E", "H", "E-H" },
            };

            Assert.Equal(new HashSet<HashSet<string>>()
            {
                new HashSet<string>() { "B", "E", "F" },
                new HashSet<string>() { "A", "C", "D" },
                new HashSet<string>() { "G" },
                new HashSet<string>() { "H" }
            }, graph.GetSCCs());
        }
    }
}
