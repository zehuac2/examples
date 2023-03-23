using System.Collections.Generic;
using Xunit;

namespace Algorithms.PriorityQueue.Tests
{
    public class PriorityQueueTest
    {
        [Fact]
        public void TestOrder()
        {
            PriorityQueue<string, int> queue = new PriorityQueue<string, int>();
            queue.Add("3", 3);
            queue.Add("2", 2);
            queue.Add("1", 1);

            var removed = queue.Pop();
            Assert.Equal(new KeyValuePair<int, string>(1, "1"), removed);

            removed = queue.Pop();
            Assert.Equal(new KeyValuePair<int, string>(2, "2"), removed);

            removed = queue.Pop();
            Assert.Equal(new KeyValuePair<int, string>(3, "3"), removed);
        }

        [Fact]
        public void TestDuplicatePriorities()
        {
            PriorityQueue<string, int> queue = new PriorityQueue<string, int>();
            queue.Add("1", 1);
            queue.Add("1", 1);
            queue.Add("2", 2);

            var removed = queue.Pop();
            Assert.Equal(new KeyValuePair<int, string>(1, "1"), removed);

            removed = queue.Pop();
            Assert.Equal(new KeyValuePair<int, string>(1, "1"), removed);

            removed = queue.Pop();

            Assert.Equal(new KeyValuePair<int, string>(2, "2"), removed);
        }

        [Fact]
        public void TestUpdate()
        {
            PriorityQueue<string, int> queue = new PriorityQueue<string, int>();
            queue.Add("update", 2);
            queue.Add("1", 1);

            queue.Update("update", 2, 0);

            Assert.Equal(new KeyValuePair<int, string>(0, "update"), queue.Pop());
            Assert.Equal(new KeyValuePair<int, string>(1, "1"), queue.Pop());
        }
    }
}
