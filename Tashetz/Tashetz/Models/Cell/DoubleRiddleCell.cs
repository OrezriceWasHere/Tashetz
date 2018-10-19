using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Models.Cell
{
    class DoubleRiddleCell : RiddleCell
    {


        public DoubleRiddleCell(string riddle1, Direction dir1, int length1, string riddle2, Direction dir2, int length2,
            int x, int y) : base(RiddleType.DOUBLE_TEXT_RIDDLE, new object[] { riddle1, dir1, riddle2, dir2 }, x, y) {

            this.Solution1 = new List<string[]>();
            this.Solution2 = new List<string[]>();
            this.Length1 = length1;
            this.Length2 = length2;

           
        }

        public string Riddle1
        {
            get
            {
                return (((Object[])this.Riddle)[0]).ToString();
            }
        }
        public string Riddle2
        {
            get
            {
                return (((Object[])this.Riddle)[2]).ToString();
            }
        }
        public Direction Direction1
        {
            get
            {
                return Direction.GetDirectionByText((((Object[])this.Riddle)[1]).ToString());
            }
        }
        public Direction Direction2
        {
            get
            {
                return Direction.GetDirectionByText((((Object[])this.Riddle)[3]).ToString());
            }
        }

        public List<String[]> Solution1
        {
            get; set;
        }

        public List<String[]> Solution2
        {
            get; set;
        }

        public int Length1
        {
            get;
        }

        public int Length2
        {
            get;
        }

        public void AddPossibleSolution1(String[] solution)
        {
            this.Solution1.Add(solution);
        }

        public void AddPossibleSolution2(String[] solution)
        {
            this.Solution2.Add(solution);
        }


        public override string ToString()
        {

            return String.Format("Double Riddle Cell ({0}, {1}):\n\trid1={2}\tdir={3}\n\trid2={4}\tdir={5}",
                this.X, this.Y, this.Riddle1, this.Direction1, this.Riddle2, this.Direction2);
        }
    }
}
