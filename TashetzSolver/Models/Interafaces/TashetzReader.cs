using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TashetzSolver.Models;

namespace TashetzSolver.Models.Interafaces
{
    interface TashetzReader
    {
        Cell.Cell[,] ReadTashetzFromApi(string api);
    }
}
