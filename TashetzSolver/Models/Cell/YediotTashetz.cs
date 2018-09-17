using System;
using TashetzSolver.Models.Interafaces;

namespace TashetzSolver.Models.Cell
{
    class YediotTashetz
    {
        public static readonly int WIDTH  = 15;
        public static readonly int HEIGHT = 12;

        private static YediotTashetz tashetz = new YediotTashetz();

        public Cell[,] cells { get; private set; }

        private YediotTashetz() {}

        private bool IsInitliazed()
        {
            return YediotTashetz.GetInstance().cells != null;
        }

        public static YediotTashetz GetInstance()
        {
            return YediotTashetz.tashetz;
        }
        
        public Cell GetCellAt(int x, int y)
        {

            if (!YediotTashetz.tashetz.IsInitliazed())
            {
                throw new Exception("Need to initialize tashetz before accessing it. " +
                                    "Use YediotTashez.InitFromApi() method.");

            }

            if (x < 0 || x > WIDTH)
            {
                throw new Exception("Impossible x value : " + x);
            }
            if (y < 0 || y > HEIGHT)
            {
                throw new Exception("Impossible y value: " + y);
            }
            return this.cells[x,y];
        }

        public static void InitFromApi(TashetzReader reader, string google_api)
        {
            YediotTashetz.GetInstance().cells = reader.ReadTashetzFromApi(google_api);
        }
    }
}
