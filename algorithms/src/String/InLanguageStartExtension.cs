using System.Text.RegularExpressions;

namespace Algorithms.String
{
    public static class InLanguageStartExtension
    {
        internal static bool IsFullMatch(this string s, string expression)
        {
            Regex regex = new Regex(expression);
            return regex.IsMatch(s);
        }

        public static bool IsInLanguageStarRecursive(
            this string s,
            string language)
        {
            if (s.Length == 0)
            {
                return true;
            }

            if (s.IsFullMatch(language))
            {
                return true;
            }

            for (int i = 0; i < s.Length - 1; i++)
            {
                if (s.Substring(0, i).IsFullMatch(language)
                    && s.Substring(i).IsInLanguageStarRecursive(language))
                {
                    return true;
                }
            }

            return false;
        }

        public static bool IsInLanguageStarIterative(
            this string s,
            string language)
        {
            bool[] results = new bool[s.Length + 1];
            results[s.Length] = true;

            for (int i = s.Length - 1; i >= 0; i--)
            {
                results[i] = false;

                for (int j = i + 1; j <= s.Length; j++)
                {
                    // (j - 1) - i + 1 = j - i
                    string slice = s.Substring(i, j - i);

                    if (slice.IsFullMatch(language) && results[j])
                    {
                        results[i] = true;
                        break;
                    }
                }
            }

            return results[0];
        }
    }
}
