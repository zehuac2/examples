using System.IO;

namespace Compiler.Syntax.Expressions
{
    public enum OperatorKind
    {
        Add
    }

    public class OperatorExpression : Expression
    {
        public OperatorKind Operator;
        public Expression Left;
        public Expression Right;

        public OperatorExpression(OperatorKind operatorKind, Expression left, Expression right)
        {
            Operator = operatorKind;
            Left = left;
            Right = right;
        }

        public override string ToString()
        {
            return $"OperatorExp(op: {Operator}, left: {Left}, right: {Right})";
        }

        public override void Print(TextWriter writer, int indent)
        {
            writer.WriteLine(
              "{0}OperatorExp(op: {1})",
              CreateIndent(indent),
              Operator);

            Left.Print(writer, indent + 2);
            Right.Print(writer, indent + 2);
        }
    }
}
