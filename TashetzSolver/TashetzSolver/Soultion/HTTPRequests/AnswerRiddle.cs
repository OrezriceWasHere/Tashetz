using System;
using System.IO;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using HtmlAgilityPack;
using System.Windows.Forms;
using System.Linq;
using System.Collections.Generic;

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

        public static readonly URLByDefinition[] URL_FORMAT = new URLByDefinition[]
        {
                BuildURL,
                BuildURLHTTPS
        };


        public static async Task<string> DownloadHTMLAsync(string definition)
        {

            foreach (var url_function in URL_FORMAT)
            {
                try
                {
                    var url = url_function(definition);
                    HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);

                    // HTTP headers are required by website
                    request.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2";

                    // Redirection occure when website cannot find solution. No use for us to allow redirect
                    request.AllowAutoRedirect = false;


                    using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                    {
                        if (response.StatusCode == HttpStatusCode.Moved || response.StatusCode == HttpStatusCode.MovedPermanently)
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

        public static async Task<string> GetAllSolutionsByDefinitionAsync(string definition)
        {
            var html = await DownloadHTMLAsync(definition);
            var html_document = new HtmlAgilityPack.HtmlDocument();
            html_document.LoadHtml(html);

            try
            {
                return html_document.DocumentNode.Descendants("p").ToArray()[3].InnerText;
            }
            catch (Exception)
            {
                return String.Empty;
            }
        }


        public static async Task<List<string>> GetSolutionByDefinitionAsync(string definition, int[] word_length)
        {
            List<string> answers = new List<string>();

            foreach (string solution in (await AnswerRiddle.GetAllSolutionsByDefinitionAsync(definition)).Split('\n'))
            {
                var line_parts = solution.Split(':');
                string description = line_parts[0].Trim();
                string wanted_description = "פתרון של " +
                    (word_length.Length == 1 ? word_length[0] : word_length.Length) + " " +
                    (word_length.Length == 1 ? "אותיות" : "מילים");


                // Hurray! we found the answer
                if (description.Equals(wanted_description))
                {

                    // Answers are seperated by ','
                    foreach (string answer in line_parts[1].Split(','))
                    {

                        // We need to make sure the answer fits in our tashetz
                        if(word_length.Length == 1)
                        {
                            if (word_length[0] == answer.Length)
                            {
                                // Make sure we remove the explanation statring in (
                                if (!answer.Contains("("))
                                {
                                    answers.Add(answer.Trim());
                                }
                                else
                                {
                                    answers.Add(answer.Substring(0, answer.IndexOf('(')));
                                }
                            }
                        }
                        else
                        {
                            string words = 
                        }


                    }

                    break;
                }

            }

            return answers;
        }
    }
}

