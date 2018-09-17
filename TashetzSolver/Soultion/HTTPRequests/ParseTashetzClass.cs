using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Soultion.HTTPRequests
{
    class ParseTashetzClass
    {
        public string[] text { get; set; }
        public int start_loc_y { get; set; }
        public int start_loc_x { get; set; }
        public int length { get; set; }
        public int y { get; set; }
        public int x { get; set; }
        public string dir { get; set; }
        public int? length_left { get; set; }
        public int? length_down { get; set; }

        public override string ToString()
        {
            return String.Format("{0},{1}:\ttext={2}\n\tstart={3},{4}\n\tdir={5}" +
                "\n\tlength={6}\n\tlength_left={7}\n\t" +
                "length_down={8}\n*******************\n",
                this.x, this.y, string.Join("", this.text), this.start_loc_x, this.start_loc_y,
                this.dir, this.length, this.length_left, this.length_down
                );
        }

    }
}
