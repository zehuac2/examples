using System;

namespace AI.Layers
{
    /// <summary>
    /// A linear layer
    ///
    /// Weights are stored in columns. There is a separate column for each
    /// output. y = 0 stores the biases
    /// </summary>
    public class LinearLayer
    {
        public Matrix Matrix { get; private set; }

        public int InputLength => this.Matrix.Height;
        public int OutputLength => this.Matrix.Width;

        public LinearLayer(int inputLength, int outputLength)
        {
            this.Matrix = new Matrix(inputLength + 1, outputLength);
        }

        /// <summary>
        /// Evaluate layer
        /// </summary>
        /// <param name="input">
        /// the input matrix, should have shape (1, input lenght + 1)
        /// </param>
        /// <returns></returns>
        public Matrix Evaluate(Matrix input)
        {
            return input * this.Matrix;
        }
    }
}
