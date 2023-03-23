using Xunit;

namespace AI.Layers.Tests
{
    public class MatrixTest
    {
        [Fact]
        public void TestEquality()
        {
            Matrix matrixA = new Matrix(2, 1)
            {
                [0, 0] = 17.0f,
                [1, 0] = 17.0f,
            };

            Matrix matrixB = new Matrix(2, 1)
            {
                [0, 0] = 17.0f,
                [1, 0] = 17.0f,
            };

            Assert.True(matrixA.Equals(matrixB));
        }

        [Fact]
        public void TestMultiplication()
        {
            Matrix a = new Matrix(2, 3)
            {
                [0, 0] = 1, [0, 1] = 2, [0, 2] = 3,
                [1, 0] = 4, [1, 1] = 5, [1, 2] = 6,
            };

            Matrix b = new Matrix(3, 2)
            {
                [0, 0] = 7, [0, 1] = 8,
                [1, 0] = 9, [1, 1] = 10,
                [2, 0] = 11, [2, 1] = 12,
            };

            Matrix expected = new Matrix(2, 2)
            {
                [0, 0] = 58, [0, 1] = 64,
                [1, 0] = 139, [1, 1] = 154,
            };

            Matrix actual = a * b;

            Assert.Equal(expected, actual);
        }
    }
}
