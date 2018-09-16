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
using TashetzSolver.Soultion;
using TashetzSolver.Soultion.HTTPRequests;

namespace TashetzSolver.Soultion
{
    class Program 
    {

        public static async Task Main()
        {
            int count = 0;
            string definition = "סינונימי בבלשנות";
            foreach(var solution in await AnswerRiddle.GetSolutionByDefinitionAsync(definition, new int [] { 3 }))
            {
                Console.WriteLine("solution is {0}", solution);
            }
            Console.ReadKey();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        }




    }
}
