using System;

namespace Compiler.Syntax.Expressions
{
    public static class TokenExtensions
    {
        public static OperatorKind ToOperatorKind(this TokenKind tokenKind)
        {
            switch (tokenKind)
            {
                case TokenKind.Add:
                    return OperatorKind.Add;
                default:
                    throw new ArgumentException();
            }
        }
    }
}
