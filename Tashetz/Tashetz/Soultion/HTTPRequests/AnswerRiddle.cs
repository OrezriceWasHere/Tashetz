using System;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Linq;
using System.Collections.Generic;
using System.Web;

namespace TashetzSolver.Soultion.HTTPRequests
{
    class AnswerRiddle
    {
        /// <summary>
        /// 'Note' is a website containing answers for riddles.
        /// Some of the solutions is delivered by HTTP and some by HTTPS.
        /// only god knows why.
        /// This is the format of HTTP solutions.
        /// </summary>
        /// <param name="definition">definition to be searched</param>
        /// <returns>URL that should have definition in http format</returns>
        public static string BuildURL(string definition)
        {
            return String.Format("http://www.note.co.il/solutions/{0}", DecodeDefinition(definition.Replace(' ', '_')));
        }

        /// <summary>
        /// HTTPS format of solution
        /// </summary>
        /// <param name="definition">definition to be searched</param>
        /// <returns>URL that should have definition in https format</returns>
        public static string BuildURLHTTPS(string definition)
        {
            return String.Format("https://www.note.co.il/solution/{0}/", DecodeDefinition(definition.Replace(' ', '-')));
        }


        /// <summary>
        /// Decode definition so it can be sent in URL.
        /// </summary>
        /// <param name="plainText">definition to be searched</param>
        /// <returns>Encoded definition</returns>
        public static string DecodeDefinition(string plainText)
        {
            return HttpUtility.UrlPathEncode(plainText.Trim());
        }


        /// <summary>
        /// A decleration of format of definition (so it can be stored in array).
        /// </summary>
        /// <param name="definition"></param>
        /// <returns></returns>
        public delegate string URLByDefinition(string definition);


        // All the url we got to look for the answer
        public static readonly URLByDefinition[] URL_FORMAT = new URLByDefinition[]
        {
                BuildURL,
                BuildURLHTTPS
        };

        /// <summary>
        /// This function downloads an HTML page which contains the solution of the relvant definition 
        /// </summary>
        /// <param name="definition">The definition we are after (an israeli singer, a bank account...) </param>
        /// <returns></returns>
        public static async Task<string> DownloadHTMLAsync(string definition)
        {
            // URL_FORMAT is basically an array of function,
            // each of which leads to a possible url where the definition could be downloaded
            foreach (var url_function in URL_FORMAT)
            {
                try
                {
                    // We invoke the funtion to recieve the url
                    var url = url_function(definition);
                    HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);

                    // HTTP headers are required by website
                    request.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2";

                    // Redirection occure when website cannot find solution. No use for us to allow redirect
                    request.AllowAutoRedirect = false;


                    using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                    {

                        // No answer for us,
                        // We better check differenet URL
                        if (response.StatusCode != HttpStatusCode.OK)
                        {
                            continue;
                        }


                        using (Stream stream = response.GetResponseStream())
                        using (StreamReader reader = new StreamReader(stream))
                        {
                            return await reader.ReadToEndAsync();
                        }
                    }

                }

                // Exception is not being able to find solution. 
                catch (Exception e)
                {
                    continue;
                }
            }

            // No solution is found
            return string.Empty;
        }

        /// <summary>
        /// This method filters the useless HTML text from the website 
        /// and leaves us only with the paragraph containing the answers.
        /// </summary>
        /// <param name="definition">The definition we are after (an israeli singer, a bank account...) </param>
        /// <returns>paragraph containing all possible answers</returns>
        public static async Task<string> GetAllSolutionsByDefinitionAsync(string definition)
        {
            // Download the HTML
            var html = await DownloadHTMLAsync(definition);

            var html_document = new HtmlAgilityPack.HtmlDocument();
            html_document.LoadHtml(html);

            try
            {

                // The answers paragraph is third (wishing the website will not change design anytime soon)
                return html_document.DocumentNode.Descendants("p").ToArray()[3].InnerText;
            }
            // So many exceptation could occur
            // no html loaded, no paragraphs, no 4 paragraph, no inner text
            catch (Exception)
            {
                return String.Empty;
            }
        }

        /// <summary>
        /// This methods download an answer to the definition give and find the relevant solution of them
        /// </summary>
        /// <param name="definition">The definition we are after (an israeli singer, a bank account...) </param>
        /// <param name="word_length">The "profile" of the answer (how many character in each word)</param>
        /// <returns>All relvant solution</returns>
        public static async Task<List<string[]>> GetSolutionByDefinitionAsync(string definition, int[] word_length)
        {
            List<string[]> answers = new List<string[]>();

            // Find all definitions online 
            var definitions_and_answers = (await AnswerRiddle.GetAllSolutionsByDefinitionAsync(definition)).Split('\n');

            // Look in any definition to find out if it fits us
            foreach (string solution in definitions_and_answers)
            {
                // Definition and answer are parted with ':' between them 
                string[] line_parts = solution.Split(':');

                // The description is the first part
                string description = line_parts[0].Trim();

                // We found a description that matches the description we are after.
                // The description is built based on word_length, which is an array stroing the lengthes 
                // of the words we are after (first item is the length of first word, and so on...)
                if (description.Equals(BuildDescription(word_length)))
                {

                    // Answers are seperated by ','
                    foreach (string answer in RemoveExplnations(line_parts[1]).Split(','))
                    {
                        // Get rid of those annoying chupchics St'aling
                        string[] answer_words = answer.Trim().Replace("'", "").Split(' ');

                        // Translate all word lengthes from strings to integers 
                        // represnting the words' length
                        var words_found_length = from word in answer_words
                                                 select word.Length;

                        // Hurray! Even the length of the word fit our demand! 
                        // That definition is ours to keep
                        if (words_found_length.SequenceEqual(word_length))
                        {
                            answers.Add(answer_words);
                        }

                    }

                    // Once we found our rellevant description, 
                    // we don't have to look anymore
                    break;
                }

            }

            return answers;
        }


        // get rid of those annoying explnations 
        // answer is sometimes like:
        // solution of 4 letters : AAAA (explnations), BBBB (explnation), CCCC
        private static string RemoveExplnations(string text)
        {

            // Validate we have a good string
            if (String.IsNullOrEmpty(text))
            {
                return String.Empty;
            }

            // Get rid of all the explnations (explnation is useless for the answer and is 
            // written between ())
            while (text.Contains('(') && text.Contains(')'))
            {
                int start = text.IndexOf('(');
                int end = text.IndexOf(')');

                // keep text before explain
                if (end != text.Length - 1)
                {
                    text = text.Substring(0, start) + text.Substring(end + 1);
                }
                else
                {
                    // keep text after explain
                    text = text.Substring(0, start);
                }

            }

            return text;
        }


        // Generate the expecated desription of the answer
        // "solution of 3 letters",
        // "solution of 2 words"
        private static string BuildDescription(int[] word_length) 
        {
            string wanted_description = "פתרון של " +
                (word_length.Length == 1 ? word_length[0] : word_length.Length) + " " +
                (word_length.Length == 1 ? "אותיות" : "מילים");

            return wanted_description;
        }

    }
}

