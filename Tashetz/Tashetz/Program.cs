
﻿using System;
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
using TashetzSolver.TashetzSolver.Soultion.Solver;
using Tashetz.Soultion.Solver;

namespace TashetzSolver.Soultion
{
    class Program
    {
        

        public static async Task Main()
        {




            
            DeleteLogFile();
            string image_dir = @"F:\Tashetz\IMG5.jpg";
            TashetzReader reader = new ParseTashetz();

            await SolutionByParts.DownloadDefinitons(FileHandler.ImageHandler.EncodeImageBase64(image_dir));



            var watch = System.Diagnostics.Stopwatch.StartNew();


            await SolutionByParts.FindSolutions();




            watch.Stop();
            var elapsedMs = watch.ElapsedMilliseconds;
            Console.WriteLine("took {0} ms to complete", elapsedMs);
            Console.ReadLine();

            return;
        }

        public static void WriteToFile(string file_name, string text)
        {
            // WriteAllText creates a file, writes the specified string to the file,
            // and then closes the file.    You do NOT need to call Flush() or Close().
            System.IO.File.AppendAllText(file_name, text + Environment.NewLine);

        }

        static string FILE_NAME = @"F:\Tashetz\parse_tashetz.txt";

        public static void WriteToLogFile(string text)
        {

            WriteToFile(FILE_NAME, text);
        }

        public static void DeleteLogFile()
        {
            System.IO.File.WriteAllText(FILE_NAME, Environment.NewLine);
        }

    }
}