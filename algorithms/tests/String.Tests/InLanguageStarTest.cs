using Xunit;

namespace Algorithms.String.Tests
{
    public class InLanguageStarTest
    {
        [Fact]
        public void TestRecursive()
        {
            Assert.True("aaa".IsInLanguageStarRecursive("a"));
            Assert.False("aaa".IsInLanguageStarRecursive("b"));
        }

        [Fact]
        public void TestIterative()
        {
            Assert.True("aaa".IsInLanguageStarIterative("a"));
            Assert.False("aaa".IsInLanguageStarIterative("b"));
        }
    }
}
