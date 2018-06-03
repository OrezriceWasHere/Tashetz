from __future__ import division

from itertools import groupby
from LinearLine import *
from os.path import join
from FileHandler import *
from Mathematics import *
import numpy
import OCRhandler
import json
import ntpath
import os



# Input source flag
IS_READING_FROM_GOOGLE = False

# Tashetz dimensions constants
ROWS = 12
COLS = 15

# All cells with two definitions
DOUBLE_DEFINITION_SQUARES = (
    (11, 4),
    (9, 8),
    (9, 1),
    (7, 3),
    (4, 1),
    (2, 9)
)

def readLine(dict_word):

    location = dict_word["boundingPoly"]["vertices"]

    x_axis = average((location[0]["x"], location[1]["x"], location[2]["x"], location[3]["x"]))
    y_axis = average((location[0]["y"], location[1]["y"], location[2]["y"], location[3]["y"]))

    return {(x_axis,y_axis):dict_word["description"]}



def getParseImageData():

    if IS_READING_FROM_GOOGLE:

        return [OCRhandler.parseTashets(join(GLOBAL_TASHETZ_DIRECTORY,file)) for file in LIST_IMAGES]


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



def getLinesInSquare(list_words_inside_square, square_x_line, square_y_line):

    if not list_words_inside_square:
        pass


    import copy
    hard_copy_list_words_inside_square = copy.deepcopy(list_words_inside_square)

    unsorted_words = list_words_inside_square
    sorted_words = []
    list_lines_word = []

    upper_right_corner_of_square = {"x" : square_x_line.x(list_words_inside_square[0]["sqaure"]["x"]),
                                    "y" : square_y_line.x(list_words_inside_square[0]["sqaure"]["y"])}

    upper_left_corner_of_square = {"x" : square_x_line.x(list_words_inside_square[0]["sqaure"]["x"] - 1),
                                   "y" : square_y_line.x(list_words_inside_square[0]["sqaure"]["y"]) }


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

            one_item_dictionary_list = list()
            one_item_dictionary_list.insert(0, starting_row_word)

            # One Line further
            list_lines_word.append(one_item_dictionary_list + all_words_in_line)

            # These words are fine!!!
            sorted_words += all_words_in_line
            for word in all_words_in_line:
                unsorted_words.remove(word)

        else:

            one_item_dictionary_list = list()
            one_item_dictionary_list.insert(0, starting_row_word)

            list_lines_word.append(one_item_dictionary_list)


        # Go to next line
        word_height = distance(starting_row_word['boundingPoly']['vertices'][1],
                               starting_row_word['boundingPoly']['vertices'][2])
        upper_right_corner_of_square['y'] += word_height

    return list_lines_word

def findTwoDefinitionCells(some_lines):


    if not some_lines:
        return []

    if len(some_lines) == 1:
        return some_lines[0]

    spaces_between_lines = []

    for line_index in range(len(some_lines) - 1):
        spaces_between_lines.append(findHeightOfLine(some_lines[line_index + 1]) - findHeightOfLine(some_lines[line_index]))

    index_of_split_line = spaces_between_lines.index(max(spaces_between_lines))
    return some_lines[:index_of_split_line + 1], some_lines[index_of_split_line + 1:]



def findHeightOfLine(line_of_words):

    find_average_height_word = lambda word: average((word['boundingPoly']['vertices'][2]["y"],
                                               word['boundingPoly']['vertices'][3]["y"]))
    average_height_words = [find_average_height_word(word) for word in line_of_words]

    return average(average_height_words)



##
def closestRectangleToPoint(point, rectagnles):

      if not rectagnles:
          return None

      calculate_distance = [ {"word" : word,
                              "distance"  : distance(point, word['boundingPoly']['vertices'][1])}

                              for word in rectagnles]

      return sorted(calculate_distance, key=lambda item: item["distance"])[0]["word"]




def parseGoogleText(google_text_json):
    response_json = json.loads(google_text_json)

    sizes = response_json["responses"][0]["textAnnotations"][0]["boundingPoly"]["vertices"]

    width = int(sizes[1]["x"]) - int(sizes[0]["x"])
    start_x = sizes[0]["x"]
    height = int(sizes[2]["y"]) - int(sizes[1]["y"])
    start_y = sizes[1]["y"]

    # In those linear lines,
    # x value is the pixel on the image(upon a single axis),
    # y value is the square of the pixel(upon that axis)
    squareX = Linearline(-COLS, width, start_x, COLS)
    squareY = Linearline(ROWS, height, start_y, 0)

    # Change to squares instead of actual x and y values
    rows = []
    for word in (response_json["responses"][0]["textAnnotations"])[1:]:
        x, y = getDimensionAverage(word)
        x = squareX.y(x)
        y = squareY.y(y)
        rows.append({'sqaure': {"x": x, "y": y},
                     'boundingPoly': word['boundingPoly'],
                     'description': word['description']})

    sortSquares = lambda item: item["sqaure"]["x"] * 100 + item["sqaure"]["y"]

    groupToSqaures = groupby(sorted(rows, key=sortSquares), key=sortSquares, )

    json_result = []

    # Group Each square in tashetz
    # key is garbage, don't use it!
    for key, text in groupToSqaures:

        lines = getLinesInSquare(list(text), squareX, squareY)

        try:
            x_square, y_square = lines[0]["sqaure"]["x"], lines[0]["sqaure"]["y"]

        #TypeError exception may be thrown because lines is two dimesional because insead of one
        except TypeError:
            x_square, y_square = lines[0][0]["sqaure"]["x"], lines[0][0]["sqaure"]["y"]


        # Only One definition in cels
        if (x_square, y_square) not in DOUBLE_DEFINITION_SQUARES:

            # We need to "smash" the two dimesional text into one dimension
            flat_lines = [item for sublist in lines for item in sublist]
            new_text = [single_word["description"] for single_word in flat_lines]
            all_text = reduce(lambda row, word: row + " " + word, new_text)

            json_result.append([{
                "x": x_square,
                "y": y_square,
                "text": all_text.encode("utf-8")
            }])

        else:

            two_definitions = []

            for block in findTwoDefinitionCells(lines):
                # We need to "smash" the two dimesional text into one dimension
                flat_lines = [item for sublist in block for item in sublist]
                new_text = [single_word["description"] for single_word in flat_lines]
                all_text = reduce(lambda row, word: row + " " + word, new_text)

                two_definitions.append({
                    "x": x_square,
                    "y": y_square,
                    "text": all_text.encode("utf-8")
                })

            json_result.append(two_definitions)



    return json_result

def main():

    verifyFilesIntegrity()
    indexGoogleDataRunning = 0

    for google_text in getParseImageData():


        Save_Analysis_Files_To_Directory(LIST_IMAGES[indexGoogleDataRunning],
                                         google_text,
                                         json.dumps(parseGoogleText(google_text), ensure_ascii=False))

        print ( json.dumps(parseGoogleText(google_text), ensure_ascii=False))

        print "done."

        indexGoogleDataRunning += 1


main()