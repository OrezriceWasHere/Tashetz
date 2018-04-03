from __future__ import division
from shutil import copy2
from itertools import groupby
import OCRhandler
import json
import math
import collections
import ntpath
import os
import sys



# Input source flag
IS_READING_FROM_GOOGLE = True




# Directories constants
global_Tashetz_directoty = os.path.join("F:\\", "Tashetz")
analysis_directory = os.path.join(global_Tashetz_directoty, "Analysis")
analysis_text_file = "analysis.txt"
google_text_file = "google.txt"


# Tashetz dimensions constants
ROWS = 12
COLS = 15


# Images global
list_images = filter(lambda dir: dir.startswith("IMG"), os.listdir(global_Tashetz_directoty))


def readLine(dict_word):

    location = dict_word["boundingPoly"]["vertices"]

    x_axis = average((location[0]["x"], location[1]["x"], location[2]["x"], location[3]["x"]))
    y_axis = average((location[0]["y"], location[1]["y"], location[2]["y"], location[3]["y"]))

    return {(x_axis,y_axis):dict_word["description"]}

        #def linearLine(deltaY, deltaX, x0, y0):
        #
        #    print "deltaY", deltaY, "deltaX", deltaX
        #    return lambda x:  int(math.floor((deltaY * 1.0 / deltaX)*(x-x0) + y0))
        #
def average(integers):
    return sum(integers) / len(integers)





# Creatae a directory regarding the analysis of an image.
# A new directory will be create under Tashetz global directory called "Analysis" (Very Original, huh?)
# And inside it a new directory will be created for each analysis of an image.
# The analysis contains (Meanwhile...) the original image, the goole API analysis,
# and parsing that analysis into squares
def Save_Analysis_Files_To_Directory(image, googleAnalysis, finalResult):



    # Create Analysis Folder
    if not os.path.exists(analysis_directory):
        os.makedirs(analysis_directory)

    print "saving results to " + analysis_directory + " ..."

    # Create the unique folder for the image
    image_name, image_extension = os.path.splitext(image)
    image_analysis_directory = os.path.join(analysis_directory, image_name)
    if not os.path.exists(image_analysis_directory):
        os.makedirs(image_analysis_directory)

    # Copy image into the new folder
    Copy_Image_To_Analysis_Directory(os.path.join(global_Tashetz_directoty, image),
                                     image_analysis_directory)

    # Copy google analysis to the new folder
    Copy_Google_To_Anaylysis_Directory(googleAnalysis, image_analysis_directory)

    # Copy software analysis to the new folder
    Copy_Final_Result_To_Analysis_Directory(finalResult, image_analysis_directory)

    print "done."

    pass

def Copy_Image_To_Analysis_Directory(imageLocation, directoryLocation):

    print "copying image " + imageLocation + " to " + directoryLocation + " ..."

    copy2(imageLocation, directoryLocation)

    print "done."

    pass

def Copy_Google_To_Anaylysis_Directory(googleAnaylsis, directoryLocation):

    print "saving google analysis to folder " + directoryLocation + " ..."

    CreateFile(googleAnaylsis, os.path.join(directoryLocation,  google_text_file))

    print "done."

    pass

def Copy_Final_Result_To_Analysis_Directory(finalResult, directoryLocation):

    print "saving local analysis to folder " + directoryLocation +  " ..."

    CreateFile(finalResult, os.path.join(directoryLocation, analysis_text_file))

    print "done."
    pass

def CreateFile(text, directory):


    with open(directory, "w") as file:
        file.write(text)

def readFromFile(directory):

    with open(directory) as file:
        return file.read()

def getGoogleData():

    if IS_READING_FROM_GOOGLE:

        return [os.path.join(global_Tashetz_directoty,OCRhandler.parseTashets(file).encode("utf-8")) for file in list_images]


    joinPaths = lambda main, dir: os.path.join(main, dir)

    findFileName = lambda dir : os.path.splitext(ntpath.basename(dir))[0]
    findGoogleFile = lambda image_dir: joinPaths(analysis_directory,joinPaths(findFileName(image_dir), google_text_file))

    answer = []

    for dir in list_images:
        answer.append(readFromFile(findGoogleFile(dir)))

    return answer



def verifyFilesIntegrity():
    if not os.path.isdir(global_Tashetz_directoty) or not list_images:
        print "Oh no! no tashetz directory in " + global_Tashetz_directoty + "\n or no image file (starts with 'IMG')! "
        print "It's such a disaster!"
        print "It's the biggest trouble so far"
        exit()


#   We compare first by x and then by y(that's why x value is bigger)!!!
#
def sortListOfWords(line):

    x_average, y_average = getDimensionAverage(line)

    return x_average * 1000 + y_average

# A shape of line is:
#   line = {
#       'boundingPoly': {
#           'vertices': [
#               {'y': val, 'x': val}
#               {'y': val, 'x': val}
#               {'y': val, 'x': val}
#               {'y': val, 'x': val}
#           ]
#       }
#       ext...
#   }
def getDimensionAverage(line):

    x_dimension = [raw['x'] for raw in line['boundingPoly']['vertices']]
    y_dimension = [raw['y'] for raw in line['boundingPoly']['vertices']]

    return average(x_dimension), average(y_dimension)


class Linearline:


    def __init__(self, deltaY, deltaX, x0, y0):
        self.derrative = deltaY / deltaX
        self.x0 = x0
        self.y0 = y0
        pass

    def y(self, x):
        return int(math.floor(self.derrative * (x - self.x0) + self.y0))




def main():

    verifyFilesIntegrity()
    indexGoogleDataRunning = 0

    for google_text in getGoogleData():



        response_json = json.loads(google_text)

        sizes = response_json["responses"][0]["textAnnotations"][0]["boundingPoly"]["vertices"]

        width = int(sizes[1]["x"]) - int(sizes[0]["x"])
        start_x = sizes[0]["x"]
        height = int(sizes[2]["y"]) - int(sizes[1]["y"])
        start_y = sizes[1]["y"]


        squareX = Linearline(COLS,width, start_x, 0)
        squareY = Linearline(ROWS,height, start_y, 0)


        response_json_to_sort = (response_json[u'responses'][0][u'textAnnotations'])[1:]

        # Sort X and Y Coordinates in values
        line_list = sorted(response_json_to_sort, key=sortListOfWords)


        rows = []
        for word in line_list:
            x , y = getDimensionAverage(word)
            x = squareX.y(x)
            y = squareY.y(y)
            rows.append({'place': (x,y), 'word':word['description'].encode("utf8")})

        string = ""


        # Group Each square in tashetz
        for place, text in groupby(rows, lambda item : item['place']):
            new_text = [single_word["word"] for single_word in text]
            all_text = reduce(lambda row, word: row + " " + word, new_text)
            string += "({0}, {1}) : {2}\n".format(place[0], place[1], all_text)


        print "done."


        Save_Analysis_Files_To_Directory(list_images[indexGoogleDataRunning],
                                         google_text,
                                         list_images[indexGoogleDataRunning] + ":\n" + string)
        indexGoogleDataRunning += 1


main()