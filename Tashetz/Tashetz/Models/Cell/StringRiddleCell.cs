using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    public class StringRiddleCell : RiddleCell
    {
        public int Start_loc_x { get; private set; }
        public int Start_loc_y { get; private set; }

        public Direction Direction_Riddle { get; private set; }

        // Length is the total amount of cells required for the answer
        // For two words and aboce, Length would contain the length of the words
        public int Length { get; private set; }

        protected internal StringRiddleCell(int x_riddle_start, int y_riddle_start, Direction dir,
            string riddle, int x, int y, int length) : base(RiddleType.TEXT_RIDDLE, riddle, x, y)
        {
            this.Start_loc_x = x_riddle_start;
            this.Start_loc_y = y_riddle_start;
            this.Direction_Riddle = dir;
            this.Length = length;
        }

        public override string ToString()
        {
            return String.Format("String riddle Cell ({0}, {1}):\n\tRiddle={2}\n\tDir={3}\n\tStartLoc={4}",
                this.X, this.Y, this.Riddle, this.Direction_Riddle, this.Start_loc_x, this.Start_loc_y);
        }
    }
}
