using System.Collections.Generic;
using Xunit;

namespace Algorithms.Set.Tests
{
    public class PowerSetTests
    {
        public static IEnumerable<object[]> GetData()
        {
            yield return new object[]
            {
                new int[][]
                {
                    new int[]{},
                    new int[]{ 1 },
                    new int[]{ 2 },
                    new int[]{ 3 },
                    new int[]{ 1, 2 },
                    new int[]{ 1, 3 },
                    new int[]{ 2, 3 },
                    new int[]{ 1, 2, 3 },
                },
                new int[] { 1, 2, 3 }
            };
        }

        [Theory]
        [MemberData(nameof(GetData), MemberType = typeof(PowerSetTests))]
        public void Test(int[][] expected, int[] set)
        {
            List<List<int>> powerset = set.GetPowerSet();

            foreach (List<int> sub in powerset)
            {
                int[] subArray = sub.ToArray();
                Assert.Contains(subArray, expected);
            }

            Assert.Equal(powerset.Count, expected.Length);
        }
    }
}
