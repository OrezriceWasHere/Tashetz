using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models
{
    public sealed class Direction
    {
        public static readonly Direction DOWN = new Direction(0, 1);
        public static readonly Direction LEFT = new Direction(1, 0);

        public int X_delta;
        public int Y_delta;

        private Direction(int x_delta, int y_delta)
        {
            this.X_delta = x_delta;
            this.Y_delta = y_delta;
        }

        public static Direction GetDirectionByText(string dir_name)
        {
            try
            {
                return typeof(Direction).GetField(dir_name.ToUpper()).GetValue(null) as Direction;
            }
            catch(NullReferenceException)
            {
                return null;
            }
        }

        public override string ToString()
        {
            return this.X_delta == DOWN.X_delta && this.Y_delta == DOWN.Y_delta ? "DOWN" : "LEFT";
        }



    }
}
