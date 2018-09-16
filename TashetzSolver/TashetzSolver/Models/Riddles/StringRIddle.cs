using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    public class StringRiddle
    {
        public byte[] Answer_legnth { get; private set; }
        public StringRiddleCell Riddle_Question { get; private set; }
        public Cell Starting_Cell { get; private set; }
        public Direction Direction { get; private set; }

        public StringRiddle(StringRiddleCell riddleCell, Direction dir, 
            byte[] answer_length, Cell start_cell)
        {
            if (answer_length == null || answer_length.Length == 0)
            {
                throw new Exception("impossible value for answer length: " + answer_length);
            }
            this.Riddle_Question = riddleCell;
            this.Direction = dir ?? throw new Exception("Impossible direction value: " + dir);
            this.Answer_legnth = answer_length;
            this.Starting_Cell = start_cell;
        }


    }
}
