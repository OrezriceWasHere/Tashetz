from __future__ import division

from itertools import groupby
from LinearLine import Linearline
from os.path import join
from FileHandler import *
from Mathematics import *
import OCRhandler
import json
import math
import collections
import ntpath
import os
import sys



# Input source flag
IS_READING_FROM_GOOGLE = False


# Tashetz dimensions constants
ROWS = 12
COLS = 15


def readLine(dict_word):

    location = dict_word["boundingPoly"]["vertices"]

    x_axis = average((location[0]["x"], location[1]["x"], location[2]["x"], location[3]["x"]))
    y_axis = average((location[0]["y"], location[1]["y"], location[2]["y"], location[3]["y"]))

    return {(x_axis,y_axis):dict_word["description"]}



def getParseImageData():

    if IS_READING_FROM_GOOGLE:

        return [OCRhandler.parseTashets(join(GLOBAL_TASHETZ_DIRECTORY,file)).encode("utf-8") for file in LIST_IMAGES]


    findFileName = lambda dir : os.path.splitext(ntpath.basename(dir))[0]
    findAnaylsisFile = lambda image_dir: join(ANALYSIS_DIRECTORY,join(findFileName(image_dir), GOOGLE_TEXT_FILE))

    answer = []

    for dir in LIST_IMAGES:
        answer.append(readFromFile(findAnaylsisFile(dir)))

    return answer





#   We compare first by x and then by y(that's why x value is bigger)!!!
#
def sortListOfWords(line):

    x_average, y_average = getDimensionAverage(line)

    return x_average  +   y_average * 1000

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





def main():

    verifyFilesIntegrity()
    indexGoogleDataRunning = 0

    for google_text in getParseImageData():



        response_json = json.loads(google_text)

        sizes = response_json["responses"][0]["textAnnotations"][0]["boundingPoly"]["vertices"]

        width = int(sizes[1]["x"]) - int(sizes[0]["x"])
        start_x = sizes[0]["x"]
        height = int(sizes[2]["y"]) - int(sizes[1]["y"])
        start_y = sizes[1]["y"]


        squareX = Linearline(COLS,width, start_x, 0)
        squareY = Linearline(ROWS,height, start_y, 0)


        response_json_to_sort = (response_json["responses"][0]["textAnnotations"])[1:]

        # Sort X and Y Coordinates in values
        line_list = sorted(response_json_to_sort, key=sortListOfWords)

        # Change to squares instead of actual x and y values
        rows = []
        for word in line_list:
            x ,y  = getDimensionAverage(word)
            x = squareX.y(x)
            y = squareY.y(y)
            rows.append({'sqaure': (x,y), 'description' : word['description'].encode("utf8")})

        string = ""


        groupToSqaures = groupby(rows, lambda item : item['sqaure'])

        print "GroupBy Result:"

        for value in groupToSqaures:
            print value


        # Group Each square in tashetz
        for sqaure, text in groupToSqaures:
            new_text = [single_word["description"] for single_word in text]
            all_text = reduce(lambda row, word: row + " " + word, new_text)
            string += "({0}, {1}) : {2}\n".format(place[0], place[1], all_text)


        print "done."


        Save_Analysis_Files_To_Directory(LIST_IMAGES[indexGoogleDataRunning],
                                         google_text,
                                         string)
        indexGoogleDataRunning += 1


main()