using System;
using System.Collections.Generic;

namespace Compiler.Syntax
{
    public class Program
    {
        static IEnumerator<Token> GetTokens()
        {
            // yield return new Token(TokenKind.Integer, 1);
            // yield return new Token(TokenKind.Add, null);
            yield return new Token(TokenKind.LeftParenthesis);
            yield return new Token(TokenKind.Integer, 1);
            yield return new Token(TokenKind.Add);
            yield return new Token(TokenKind.Integer, 1);
            yield return new Token(TokenKind.RightParenthesis);
            // yield return new Token(TokenKind.Add, null);
            // yield return new Token(TokenKind.Integer, 1);
        }

        public static void Main(string[] args)
        {
            var parser = new Parser();
            var expression = parser.Parse(GetTokens());

            expression.Print(Console.Out, 0);
        }
    }
}
