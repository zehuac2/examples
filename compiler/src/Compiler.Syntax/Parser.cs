using System;
using System.Collections.Generic;
using Compiler.Syntax.Expressions;
using Compiler.Syntax.Exceptions;

namespace Compiler.Syntax
{
    public sealed class Parser
    {
        public Expression Parse(IEnumerator<Token> tokens)
        {
            return Exp(tokens);
        }

        private Expression Exp(IEnumerator<Token> tokens)
        {
            if (!tokens.MoveNext())
            {
                throw new UnexpectedEOFException();
            }

            Token first = tokens.Current;

            switch (first.Kind)
            {
                case TokenKind.Integer:
                    Expression expPrime = ExpPrime(tokens);

                    if (!tokens.MoveNext())
                    {
                        throw new ExpectedEOFException();
                    }

                    return expPrime;
                case TokenKind.LeftParenthesis:
                    Expression exp = Parse(tokens);

                    if (!tokens.MoveNext())
                    {
                        throw new UnexpectedEOFException();
                    }

                    return exp;
                default:
                    return ExpPrime(tokens);
            }
        }

        private Expression ExpPrime(IEnumerator<Token> tokens)
        {
            Token first = tokens.Current;

            switch (first.Kind)
            {
                case TokenKind.Add:
                    return new OperatorExpression(
                        first.Kind.ToOperatorKind(),
                        new IntegerExpression((int)first.Value!),
                        Parse(tokens));
                case TokenKind.Integer:
                    return new IntegerExpression((int)first.Value!);
                default:
                    throw new Exception();
            }
        }
    }
}
