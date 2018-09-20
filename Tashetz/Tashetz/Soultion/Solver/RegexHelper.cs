using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TashetzSolver.Models.Cell;
using TashetzSolver.Soultion.HTTPRequests;
using System.Text.RegularExpressions;


namespace TashetzSolver.TashetzSolver.Soultion.Solver
{
    class RegexHelper
    {

        // This function is used to determine the length of the 
        // words, in case the answer contains more then one word.
        // The definition should include the split between words.
        // Example: "A bank account <b>(4,4)</b>"
        // The function looks for the part in the answer where the lengthes are written
        // and return it.
        // In case the definition does not include specification 
        // of word length, it is assumed to be one word, therefore the total 
        // length of cells is retunred as a one item array
        public static int[] FindWordsCount(StringRiddleCell cell)
        {
            int[] answer;

            // Content validation
            if (cell == null || cell.Riddle == null || cell.Riddle.Equals(ParseTashetz.UNRESOLVED_STRING))
            {
                answer = new int[0];
            }
            else
            {
                string riddle = cell.Riddle.ToString();

               
                string FIND_COUNT_PATTERN = @"((\d,)+\d)";
                Regex regex = new Regex(FIND_COUNT_PATTERN);
                string result = regex.Match(riddle).Value;

                if (String.IsNullOrEmpty(result))
                {
                    answer = new int[1] { cell.Length };
                }

                else
                {
                    result = result.Replace(" ", "");
                    answer = (from count in result.Split(',')
                              select int.Parse(count)).ToArray();

                    // cell.Legnth is an integer describing
                    // how many character the answer should include.
                    // The answer cannot contain a number of characters
                    // different from cell.length
                    if (answer.Sum() != cell.Length)
                    {
                        answer = new int[0];
                    }
                }
            }

            return answer;
        }
    }
}
