using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    class AnswerCell : Cell
    {
        public char Answer { get; set; }
        
        protected internal AnswerCell(int x, int y) : base(x, y){}

        public void Update_Answer(char answer)
        {
            this.Answer = answer;
        }
    }
}
