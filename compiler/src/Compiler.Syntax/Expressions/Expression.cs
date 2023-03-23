using System.IO;
using System.Text;

namespace Compiler.Syntax.Expressions
{
    public class Expression
    {
        public virtual void Print(TextWriter writer, int indent) { }

        protected string CreateIndent(int indent)
        {
            var builder = new StringBuilder();

            for (int i = 0; i < indent; i++)
            {
                builder.Append('-');
            }

            return builder.ToString();
        }
    }
}
