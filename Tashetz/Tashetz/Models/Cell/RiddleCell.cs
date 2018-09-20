using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    public abstract class RiddleCell : Cell
    {
        public object Riddle { get; private set; }
        public RiddleType QuestionType { get; private set; }

        protected internal RiddleCell(RiddleType type, object riddle, int x, int y) : base(x, y)
        {
            if (! riddle.GetType().Equals(type.RiddleQuestionType)) {
                throw new Exception(String.Format("Type mismatch: riddle type {0} cannot contatin variable" +
                    "whose type is {1}", type.RiddleQuestionType, riddle.GetType()));
            }
            this.QuestionType = type;
            this.Riddle = riddle;
        }

        
    }
}
