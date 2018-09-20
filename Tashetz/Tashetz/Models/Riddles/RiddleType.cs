using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models
{
    public sealed class RiddleType
    {
        
        public static readonly RiddleType TEXT_RIDDLE = new RiddleType(typeof(String));
        public static readonly RiddleType DOUBLE_TEXT_RIDDLE = new RiddleType(typeof(object[]));

        public Type RiddleQuestionType { get; private set; }

        private RiddleType(Type riddleType)
        {
            RiddleQuestionType = riddleType;
        }

        public override string ToString()
        {
            return RiddleQuestionType.ToString();
        }
    }
}
