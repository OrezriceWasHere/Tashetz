using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TashetzSolver.Soultion.FileHandler
{
    class ImageHandler
    {

        public static string EncodeImageBase64(string file_location)
        {
            byte[] imageArray = System.IO.File.ReadAllBytes(file_location);
            return Convert.ToBase64String(imageArray);
        }



    }
}
