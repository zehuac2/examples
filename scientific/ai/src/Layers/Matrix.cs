using System;
using System.Collections;
using System.Collections.Generic;

namespace AI.Layers
{
    public class Matrix: IEquatable<Matrix>, IEnumerable<float[]>
    {
        float[][] _values;

        public int Height => _values.Length;
        public int Width => _values[0].Length;

        public Matrix(int height, int width)
        {
            if (height == 0)
            {
                throw new ArgumentException("height cannot be 0");
            }

            if (width == 0)
            {
                throw new ArgumentException("width cannot be 0");
            }

            _values = new float[height][];

            for (int i = 0; i < height; i++)
            {
                _values[i] = new float[width];
            }
        }

        public Matrix(params float[] values)
        {
            _values = new float[][] { values };
        }

        public bool Equals(Matrix other)
        {
            if (this.Height != other.Height) { return false; }
            if (this.Width != other.Width) { return false; }

            for (int y = 0; y < this.Height; y++)
            {
                for (int x = 0; x < this.Width; x++)
                {
                    if (this[y, x] != other[y, x])
                    {
                        return false;
                    }
                }
            }

            return true;
        }

        public IEnumerator<float[]> GetEnumerator()
        {
            return _values.GetEnumerator() as IEnumerator<float[]>;
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return _values.GetEnumerator();
        }

        public float this[int y, int x]
        {
            get
            {
                return _values[y][x];
            }
            set
            {
                _values[y][x] = value;
            }
        }

        /// <summary>
        /// Multiply a by b (a * b)
        /// </summary>
        /// <param name="left">left hand side matrix</param>
        /// <param name="right">right hand side matrix</param>
        /// <returns>
        /// A new matrix
        /// </returns>
        public static Matrix operator*(Matrix left, Matrix right)
        {
            if (left.Width != right.Height)
            {
                throw new ArgumentException("a.Width must be equal to b.Height");
            }

            float[][] leftValues = left._values;
            float[][] rightValues = right._values;

            Matrix output = new Matrix(left.Height, right.Width);

            for (int y = 0; y < output.Height; y++)
            {
                for (int x = 0; x < output.Width; x++)
                {
                    float sum = 0.0f;

                    for (int i = 0; i < left.Width; i++)
                    {
                        sum += leftValues[y][i] * rightValues[i][x];
                    }

                    output[y, x] = sum;
                }
            }

            return output;
        }
    }
}
