using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace Compiler.Syntax
{
    /// <summary>
    /// A container for tokens that allows peaking
    /// </summary>
    public sealed class TokenStream : IEnumerator<Token>
    {
        private IEnumerator<Token> _source;
        private Queue<Token> _buffer = new Queue<Token>();

        public Token Current
        {
            get
            {
                if (_buffer.Count <= 0)
                {
                    return _source.Current;
                }

                return _buffer.Peek();
            }
        }

        object IEnumerator.Current => Current;

        public TokenStream(IEnumerator<Token> source)
        {
            _source = source;
        }

        /// <summary>
        /// Peak <c>distance</c> into the token stream
        /// </summary>
        /// <param name="distance">
        /// How long to peek into; if <c>distance</c> is 0, then this is equivalent of
        /// calling <c>Current</c>
        /// </param>
        /// <returns></returns>
        public Token Peek(int distance)
        {
            while (distance + 1 > _buffer.Count)
            {
                _buffer.Enqueue(_source.Current);

                if (!_source.MoveNext())
                {
                    break;
                }
            }

            return _buffer.Skip(distance).First();
        }

        /// <summary>
        /// Move <c>Current</c> to the next token
        /// </summary>
        /// <remarks>
        /// Must be called before accessing the first token
        /// </remarks>
        /// <returns></returns>
        public bool MoveNext()
        {
            if (_buffer.Count > 0)
            {
                _buffer.Dequeue();
                return true;
            }

            return _source.MoveNext();
        }

        public void Reset()
        {
            _buffer.Clear();
            _source.Reset();
        }

        public void Dispose()
        {
            _buffer.Clear();
            _source.Dispose();
        }
    }
}
