using Xunit;

namespace AI.Layers.Tests
{
    public class LinearLayerTest
    {
        [Fact]
        public void Test1()
        {
            LinearLayer layer = new LinearLayer(2, 2);

            // Bias
            layer.Matrix[0, 0] = 100.0f;
            // Weights
            layer.Matrix[1, 0] = 1.0f;
            layer.Matrix[2, 0] = 7.0f;

            // Bias
            layer.Matrix[0, 1] = 50.0f;
            // Weights
            layer.Matrix[1, 1] = 1.0f;
            layer.Matrix[2, 1] = 0.0f;

            Matrix input = new Matrix(1.0f, 1.0f, 1.0f);
            Matrix output = layer.Evaluate(input);

            Assert.Equal(new Matrix(108.0f, 51.0f), output);
        }
    }
}
