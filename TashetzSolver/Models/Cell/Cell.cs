using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    public abstract class Cell
    {
        public int X { get; private set; }
        public int Y { get; private set; }

        protected internal Cell(int x, int y)
        {
            this.X = x;
            this.Y = y;
        }

        public override bool Equals(object obj)
        {
            if (!(obj is Cell convertedObj)) {
                return false;
            }
            return convertedObj.X == this.X && convertedObj.Y == this.Y;
        }

        public override int GetHashCode()
        {
            var hashCode = 1861411795;
            hashCode = hashCode * -1521134295 + X.GetHashCode();
            hashCode = hashCode * -1521134295 + Y.GetHashCode();
            return hashCode;
        }

        public override string ToString()
        {
            return String.Format("Cell Location: ({0}, {1})", this.X, this.Y);
        }
    }
}
