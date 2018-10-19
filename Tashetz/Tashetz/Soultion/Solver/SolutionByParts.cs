using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TashetzSolver.Models.Cell;
using TashetzSolver.Models.Interafaces;
using TashetzSolver.Soultion.HTTPRequests;
using TashetzSolver.TashetzSolver.Soultion.Solver;

namespace Tashetz.Soultion.Solver
{
    class SolutionByParts
    {
        /// <summary>
        /// Get all the definitions of the tashetz and build it inside the memory.
        /// </summary>
        /// <param name="Encoded_Image">The image, encoded to base 64</param>
        /// <returns>Fill the singleton YediotTashetz, contiaing the definitions</returns>
        public static async Task DownloadDefinitons(string Encoded_Image)
        {
            // parse the tashetz from pixels (as it is an image) into strings, 
            // describing the content of the cells.
            // the answer is the raw JSON format of the parsed tashetz. 
            string google_analysis = await ParseTashetz.PostParseTashetz(Encoded_Image);

            // Load the tashetz from the API into the memory,
            // parse it from json to relevant classes
            TashetzReader reader = new ParseTashetz();
            YediotTashetz.InitFromApi(reader, google_analysis);
        }

        /// <summary>
        /// Find a solution to the definitions.
        /// This function is heavy so it is recomended to be run at background Thread.
        /// </summary>
        /// <returns>Solutions to definitions, found on the cells</returns>
        public static async Task FindSolutions()
        {
            // There is no importance to the order of getting the solutions of
            // the definitions, rather then the speed it took.
            // Parallel.For allows each iteration to run at parralel,
            // making it useful when it comes to speed.
            Parallel.For(0, YediotTashetz.WIDTH, (x) => {
                Parallel.For(0, YediotTashetz.HEIGHT, async (y) => {

                    switch (YediotTashetz.GetInstance().GetCellAt(x, y))
                    {
                        case StringRiddleCell riddleCell:


                            var riddle = riddleCell.Riddle.ToString();

                            riddle = AnswerRiddle.RemoveExplnations(riddle);
                            var words_length = RegexHelper.FindWordsCount(riddle, riddleCell.Length);

                            var solution = await AnswerRiddle.GetSolutionByDefinitionAsync(riddle, words_length);

                            foreach (var solution_one in solution)
                            {
                                riddleCell.AddPossibleSolution(solution_one);
                            }

                            break;

                        case DoubleRiddleCell doubleRiddle:
                            var riddle1 = doubleRiddle.Riddle1;
                            var riddle2 = doubleRiddle.Riddle2;

                            riddle1 = AnswerRiddle.RemoveExplnations(riddle1);
                            riddle2 = AnswerRiddle.RemoveExplnations(riddle2);

                            var words_length1 = RegexHelper.FindWordsCount(riddle1, doubleRiddle.Length1);
                            var words_legnth2 = RegexHelper.FindWordsCount(riddle2, doubleRiddle.Length2);

                            var solution1 = await AnswerRiddle.GetSolutionByDefinitionAsync(riddle1, words_length1);
                            var solution2 = await AnswerRiddle.GetSolutionByDefinitionAsync(riddle2, words_legnth2);


                            foreach (var solution_one in solution1)
                            {
                                doubleRiddle.AddPossibleSolution1(solution_one);
                            }

                            foreach (var solution_one in solution2)
                            {
                                doubleRiddle.AddPossibleSolution2(solution_one);
                            }


                            break;
                    }
                });
            });
        }


    }
}
