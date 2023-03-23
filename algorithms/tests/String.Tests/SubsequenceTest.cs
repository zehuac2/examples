using System;
using Xunit;

namespace Algorithms.String.Tests
{
    public class SubsequenceTest
    {
        [Theory]
        [InlineData(3, new int[] { int.MinValue, 1, 2, 3 })]
        [InlineData(4, new int[] { int.MinValue, 2, 3, 3, 2, 4, 5 })]
        public void TestLongestIncreasingSubsequence(int length, int[] values)
        {
            Assert.Equal(length, values.LongestIncreasingSubsequenceRecursive());
        }
    }
}
