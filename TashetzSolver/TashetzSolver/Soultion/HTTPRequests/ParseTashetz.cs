using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using TashetzSolver.Models.Cell;
using TashetzSolver.Models.Interafaces;
using System.Collections.Specialized;
using System.Net;
using Newtonsoft.Json;
using System.IO;
using TashetzSolver.Models;

namespace TashetzSolver.Soultion.HTTPRequests
{
    class ParseTashetz : TashetzReader
    {
        public static readonly string UNRESOLVED_STRING = "UNRESOLVED";

        public static string PostParseTashetz(string file_64_encoded)
        {
            using (WebClient client = new WebClient())
            {

                var encoded_image = file_64_encoded;
                var parameters = new NameValueCollection()
                {
                    { "base_64_image",  encoded_image},
                };

                
                byte[] response = client.UploadValues("http://localhost:8080/getTashetzParseImage", parameters);

                return System.Text.Encoding.UTF8.GetString(response);
            }
        }

        public Cell[,] ReadTashetzFromApi(string api)
        {
            var cells = new Cell[YediotTashetz.WIDTH, YediotTashetz.HEIGHT];
            for (int i = 0; i < YediotTashetz.WIDTH; i++)
            {
                for (int j = 0; j < YediotTashetz.HEIGHT; j++)
                {
                    cells[i, j] = new AnswerCell(i, j);
                }
            }

            var converter = JsonConvert.DeserializeObject<ParseTashetzClass[]>(api);


            using (StreamWriter outputFile = new StreamWriter(@"C:\Users\Or\Desktop\parse_tashetz.txt"))
            {
                foreach (var cell in converter)
                {

                    // Only happens to one definition cell
                    if (cell.text.Count() == 1)
                    {
                        cells[cell.x, cell.y] = new StringRiddleCell(cell.start_loc_x, cell.start_loc_y,
                            Direction.GetDirectionByText(cell.dir), cell.text[0], cell.x, cell.y);
                    }
                    else
                    {
                        cells[cell.x, cell.y] = new DoubleRiddleCell(cell.text[0],
                            Direction.LEFT, cell.text[1], Direction.DOWN, cell.x, cell.y);
                    }

                    outputFile.WriteLine(cell);

                }
            }

            return cells;
        }
    }
}
