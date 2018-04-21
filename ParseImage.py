from __future__ import division

from itertools import groupby
from LinearLine import *
from os.path import join
from FileHandler import *
from Mathematics import *
import OCRhandler
import json
import ntpath
import os



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


#   Words do not return sorted to squares. Tashetz has to handle it.
#   You take the upper right corner of the square and find closest word.
#   From there, you take the middle of the rectangle of the word and find words
#   in the same row.
#   Then you go one row down and do the same logic
def sortWordsInsideSquare(list_words_inside_square, square_x_line, square_y_line):

    if not list_words_inside_square:
        pass

    unsorted_words = list_words_inside_square
    sorted_words = []

    upper_right_corner_of_square = {"x" : square_x_line.x(list_words_inside_square[0]["sqaure"][0] + 1),
                                    "y" : square_y_line.x(list_words_inside_square[0]["sqaure"][1])}

    upper_left_corner_of_square = {"x" : square_x_line.x(list_words_inside_square[0]["sqaure"][0]),
                                   "y" : square_y_line.x(list_words_inside_square[0]["sqaure"][1]) }


    while unsorted_words:

        # Choose upper the upper right point
        starting_row_word = closestRectangleToPoint(upper_right_corner_of_square, unsorted_words)

        middle_point_right_side = middlePoint(starting_row_word['boundingPoly']['vertices'][1],
                                              starting_row_word['boundingPoly']['vertices'][2])
        unsorted_words.remove(starting_row_word)
        sorted_words.append(starting_row_word)

        # Find the row of all words in the line
        words_Linear_Line = Linearline(upper_left_corner_of_square['y'] - upper_right_corner_of_square['y'],
                                       upper_left_corner_of_square['x'] - upper_right_corner_of_square['x'],
                                       middle_point_right_side['x'], middle_point_right_side['y'])
        # Order the words in line
        all_words_in_line = [ {"distance": words_Linear_Line.intersectWithSection(word['boundingPoly']['vertices'][1],
                                                                                  word['boundingPoly']['vertices'][2]),
                               "word": word}
                              for word in unsorted_words]

        # Remove all words not in the line
        all_words_in_line = filter(lambda item: item["distance"] != Linearline.NO_INTERSECTION, all_words_in_line)

        if all_words_in_line:
            # Sort the words in coorect order
            all_words_in_line = sorted(all_words_in_line, key=lambda item: item["distance"])

            # We No Longer need the "distance"
            all_words_in_line = [word["word"] for word in all_words_in_line]

            # These words are fine!!!
            sorted_words += all_words_in_line
            for word in all_words_in_line:
                unsorted_words.remove(word)

        # Go to next line
        word_height = distance(starting_row_word['boundingPoly']['vertices'][1],
                               starting_row_word['boundingPoly']['vertices'][2])
        upper_right_corner_of_square['y'] += word_height



    return sorted_words



##
def closestRectangleToPoint(point, rectagnles):

      if not rectagnles:
          return None

      calculate_distance = [ {"word" : word,
                              "distance"  : distance(point, word['boundingPoly']['vertices'][1])}

                              for word in rectagnles]

      return sorted(calculate_distance, key=lambda item: item["distance"])[0]["word"]



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
            rows.append({'sqaure': (x,y),
                         'boundingPoly': word['boundingPoly'],
                         'description' : word['description'].encode("utf8")})

        string = ""


        groupToSqaures = groupby(sorted(rows, key=lambda item: item['sqaure']), key=lambda item : item['sqaure'])

        print "GroupBy Result:"

        sorted_words
        # Group Each square in tashetz
        for sqaure, text in groupToSqaures:

            text = sortWordsInsideSquare(list(text), squareX, squareY)
            new_text = [single_word["description"] for single_word in text]
            all_text = reduce(lambda row, word: row + " " + word, new_text)
            string += "({0}, {1}) : {2}\n".format(sqaure[0], sqaure[1], all_text)


        print "done."


        Save_Analysis_Files_To_Directory(LIST_IMAGES[indexGoogleDataRunning],
                                         google_text,
                                         string)
        indexGoogleDataRunning += 1


main()