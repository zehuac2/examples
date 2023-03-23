using System.IO;

namespace Compiler.Syntax.Expressions
{
    public class IntegerExpression : Expression
    {
        public int Value;

        public IntegerExpression(int value)
        {
            Value = value;
        }

        public override string ToString()
        {
            return $"IntegerExp({Value})";
        }

        public override void Print(TextWriter writer, int indent)
        {
            writer.WriteLine("{0}IntegerExp({1})", CreateIndent(indent), Value);
        }
    }
}
