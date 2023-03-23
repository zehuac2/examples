using System;

namespace Algorithms.String
{
    public static class SubsequenceExtension
    {
        static int _LongestIncreasingSubsequence(int[] values, int i, int j)
        {
            if (j > values.Length - 1)
            {
                return 0;
            }

            if (values[i] >= values[j])
            {
                return _LongestIncreasingSubsequence(values, i, j + 1);
            }

            return Math.Max(
                _LongestIncreasingSubsequence(values, i, j + 1),
                1 + _LongestIncreasingSubsequence(values, j, j + 1));
        }

        public static int LongestIncreasingSubsequenceRecursive(this int[] values)
        {
            return _LongestIncreasingSubsequence(values, 0, 1);
        }
    }
}
