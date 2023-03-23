using System.Collections.Generic;
using Xunit;

namespace Compiler.Syntax.Tests
{
    public class TokenStreamTests
    {
        IEnumerator<Token> GetTokens()
        {
            yield return new Token(TokenKind.Add);
            yield return new Token(TokenKind.LeftParenthesis);
            yield return new Token(TokenKind.RightParenthesis);
        }

        [Fact]
        public void Initialization()
        {
            var stream = new TokenStream(GetTokens());
            stream.MoveNext();

            Assert.Equal(new Token(TokenKind.Add), stream.Current);
        }

        [Fact]
        public void PeekAndCurrent()
        {
            var stream = new TokenStream(GetTokens());
            stream.MoveNext();

            Assert.Equal(new Token(TokenKind.Add), stream.Peek(0));
            Assert.Equal(new Token(TokenKind.Add), stream.Current);

            Assert.Equal(new Token(TokenKind.LeftParenthesis), stream.Peek(1));
            Assert.Equal(new Token(TokenKind.RightParenthesis), stream.Peek(2));

            Assert.Equal(new Token(TokenKind.Add), stream.Current);
        }

        [Fact]
        public void MoveNext()
        {
            var stream = new TokenStream(GetTokens());

            Assert.True(stream.MoveNext());
            Assert.Equal(new Token(TokenKind.Add), stream.Current);

            Assert.True(stream.MoveNext());
            Assert.Equal(new Token(TokenKind.LeftParenthesis), stream.Current);

            Assert.True(stream.MoveNext());
            Assert.Equal(new Token(TokenKind.RightParenthesis), stream.Current);

            Assert.False(stream.MoveNext());
        }

        [Fact]
        public void PeekAndMoveNext()
        {
            var stream = new TokenStream(GetTokens());
            stream.MoveNext();
            stream.Peek(1);

            Assert.Equal(new Token(TokenKind.Add), stream.Current);

            Assert.True(stream.MoveNext());
            Assert.Equal(new Token(TokenKind.LeftParenthesis), stream.Current);
        }
    }
}
