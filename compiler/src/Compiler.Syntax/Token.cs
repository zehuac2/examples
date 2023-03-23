using System;

namespace Compiler.Syntax
{
    public enum TokenKind
    {
        Add,
        Minus,
        LeftParenthesis,
        RightParenthesis,
        Integer
    }

    public struct Token : IEquatable<Token>
    {
        public TokenKind Kind;
        public object? Value;

        public Token(TokenKind kind) : this(kind, null) { }

        public Token(TokenKind kind, object? value)
        {
            Kind = kind;
            Value = value;
        }

        public override string ToString()
        {
            return $"Token({Kind}: '{Value}')";
        }

        public bool Equals(Token other)
        {
            if (Kind != other.Kind)
            {
                return false;
            }

            if (Value == null && other.Value != null)
            {
                return false;
            }

            if (Value != null && other.Value == null)
            {
                return false;
            }

            if (Value == null && other.Value == null)
            {
                return true;
            }

            return Value!.Equals(other.Value);
        }
    }
}
