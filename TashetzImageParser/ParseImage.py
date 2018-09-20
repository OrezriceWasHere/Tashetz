from __future__ import division

from itertools import groupby
from LinearLine import *
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
UNRESOLVED_TEXT = "UNRESOLVED"

# All cells with two definitions
DOUBLE_DEFINITION_SQUARES = (

    {"x": 11, "y": 4, "length_left": 4, "length_down": 2},
    {"x": 9, "y": 8, "length_left": 3, "length_down": 3},
    {"x": 9, "y": 1, "length_left": 4, "length_down": 2},
    {"x": 7, "y": 3, "length_left": 6, "length_down": 3},
    {"x": 4, "y": 1, "length_left": 4, "length_down": 2},
    {"x": 2, "y": 9, "length_left": 3, "length_down": 2}

)

ONE_DEFINITON_SQUARES = (

    {"x": 0, "y": 0, "start_loc_x": 1, "start_loc_y": 0, "dir": "down", "length": 7},
    {"x": 0, "y": 1, "start_loc_x": 1, "start_loc_y": 1, "dir": "left", "length": 3},
    {"x": 0, "y": 3, "start_loc_x": 0, "start_loc_y": 4, "dir": "left", "length": 5},
    {"x": 0, "y": 4, "start_loc_x": 0, "start_loc_y": 5, "dir": "left", "length": 4},
    {"x": 0, "y": 6, "start_loc_x": 1, "start_loc_y": 6, "dir": "left", "length": 5},
    {"x": 0, "y": 7, "start_loc_x": 0, "start_loc_y": 8, "dir": "left", "length": 4},
    {"x": 0, "y": 9, "start_loc_x": 0, "start_loc_y": 10, "dir": "left", "length": 4},
    {"x": 0, "y": 11, "start_loc_x": 1, "start_loc_y": 11, "dir": "left", "length": 2},
    {"x": 2, "y": 0, "start_loc_x": 3, "start_loc_y": 0, "dir": "down", "length": 11},
    {"x": 2, "y": 2, "start_loc_x": 3, "start_loc_y": 2, "dir": "left", "length": 8},
    {"x": 2, "y": 4, "start_loc_x": 3, "start_loc_y": 4, "dir": "down", "length": 4},
    {"x": 3, "y": 11, "start_loc_x": 4, "start_loc_y": 11, "dir": "left", "length": 2},
    {"x": 4, "y": 0, "start_loc_x": 5, "start_loc_y": 0, "dir": "down", "length": 3},
    {"x": 4, "y": 4, "start_loc_x": 5, "start_loc_y": 4, "dir": "left", "length": 4},
    {"x": 4, "y": 5, "start_loc_x": 5, "start_loc_y": 5, "dir": "left", "length": 3},
    {"x": 4, "y": 7, "start_loc_x": 5, "start_loc_y": 7, "dir": "left", "length": 2},
    {"x": 4, "y": 8, "start_loc_x": 5, "start_loc_y": 10, "dir": "left", "length": 3},
    {"x": 5, "y": 3, "start_loc_x": 5, "start_loc_y": 4, "dir": "down", "length": 8},
    {"x": 6, "y": 0, "start_loc_x": 6, "start_loc_y": 1, "dir": "down", "length": 5},
    {"x": 6, "y": 6, "start_loc_x": 6, "start_loc_y": 7, "dir": "down", "length": 2},
    {"x": 6, "y": 9, "start_loc_x": 7, "start_loc_y": 9, "dir": "left", "length": 4},
    {"x": 6, "y": 11, "start_loc_x": 7, "start_loc_y": 11, "dir": "left", "length": 3},
    {"x": 7, "y": 0, "start_loc_x": 7, "start_loc_y": 1, "dir": "down", "length": 2},
    {"x": 7, "y": 7, "start_loc_x": 7, "start_loc_y": 8, "dir": "down", "length": 4},
    {"x": 8, "y": 0, "start_loc_x": 8, "start_loc_y": 1, "dir": "down", "length": 4},
    {"x": 8, "y": 5, "start_loc_x": 9, "start_loc_y": 5, "dir": "left", "length": 4},
    {"x": 8, "y": 6, "start_loc_x": 9, "start_loc_y": 6, "dir": "left", "length": 6},
    {"x": 8, "y": 7, "start_loc_x": 8, "start_loc_y": 8, "dir": "down", "length": 2},
    {"x": 8, "y": 10, "start_loc_x": 9, "start_loc_y": 10, "dir": "left", "length": 2},
    {"x": 9, "y": 0, "start_loc_x": 10, "start_loc_y": 0, "dir": "down", "length": 4},
    {"x": 9, "y": 4, "start_loc_x": 9, "start_loc_y": 5, "dir": "down", "length": 3},
    {"x": 10, "y": 4, "start_loc_x": 10, "start_loc_y": 5, "dir": "down", "length": 2},
    {"x": 10, "y": 11, "start_loc_x": 11, "start_loc_y": 11, "dir": "left", "length": 11},
    {"x": 11, "y": 0, "start_loc_x": 12, "start_loc_y": 0, "dir": "down", "length": 7},
    {"x": 11, "y": 2, "start_loc_x": 12, "start_loc_y": 2, "dir": "left", "length": 3},
    {"x": 11, "y": 9, "start_loc_x": 12, "start_loc_y": 9, "dir": "left", "length": 3},
    {"x": 11, "y": 10, "start_loc_x": 12, "start_loc_y": 10, "dir": "left", "length": 3},
    {"x": 12, "y": 7, "start_loc_x": 12, "start_loc_y": 8, "dir": "down", "length": 4},
    {"x": 13, "y": 0, "start_loc_x": 13, "start_loc_y": 1, "dir": "down", "length": 4},
    {"x": 13, "y": 5, "start_loc_x": 13, "start_loc_y": 6, "dir": "down", "length": 2},
    {"x": 13, "y": 8, "start_loc_x": 13, "start_loc_y": 9, "dir": "down", "length": 3},
    {"x": 14, "y": 0, "start_loc_x": 14, "start_loc_y": 1, "dir": "down", "length": 2},
    {"x": 14, "y": 3, "start_loc_x": 14, "start_loc_y": 4, "dir": "down", "length": 3},
    {"x": 14, "y": 7, "start_loc_x": 14, "start_loc_y": 8, "dir": "down", "length": 4},

)

def readLine(dict_word):

    location = dict_word["boundingPoly"]["vertices"]

    x_axis = average((location[0]["x"], location[1]["x"], location[2]["x"], location[3]["x"]))
    y_axis = average((location[0]["y"], location[1]["y"], location[2]["y"], location[3]["y"]))

    return {(x_axis,y_axis):dict_word["description"]}



def getParseImageData():

    if IS_READING_FROM_GOOGLE:

        return [OCRhandler.parseTashets(join(GLOBAL_TASHETZ_DIRECTORY, file)) for file in LIST_IMAGES]


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


# This function is used when there are two definitions per one definition cell.
# You find the furthest lines that are next each other and split one definition from another
def findTwoDefinitionCells(some_lines):

    if not some_lines:
        return []

    if len(some_lines) == 1:
        return some_lines

    spaces_between_lines = []

    # Calculate height to next line
    for line_index in range(len(some_lines) - 1):
        spaces_between_lines.append(findHeightOfLine(some_lines[line_index + 1]) - findHeightOfLine(some_lines[line_index]))

    index_of_split_line = spaces_between_lines.index(max(spaces_between_lines))
    return some_lines[:index_of_split_line + 1], some_lines[index_of_split_line + 1:]

# This functuin is used to calculate the height of a line
def findHeightOfLine(line_of_words):

    POINT_RIGHT_DOWN_INDEX = 2
    POINT_RIGHT_LEFT_INDEX = 3

    find_average_height_word = lambda word: average((word['boundingPoly']['vertices'][POINT_RIGHT_DOWN_INDEX]["y"],
                                               word['boundingPoly']['vertices'][POINT_RIGHT_LEFT_INDEX]["y"]))
    average_height_words = [find_average_height_word(word) for word in line_of_words]

    return average(average_height_words)



## Find the closest word to the edge of the cell (right up)
def closestRectangleToPoint(point, rectagnles):

      if not rectagnles:
          return None

      calculate_distance = [ {"word" : word,
                              "distance"  : distance(point, word['boundingPoly']['vertices'][1])}
                              for word in rectagnles]

      return sorted(calculate_distance, key=lambda item: item["distance"])[0]["word"]

## Find in double definition cells a square with specific x and y values
def double_definition_by_x_and_y(x_square, y_square):
    cell = [dict for dict in DOUBLE_DEFINITION_SQUARES if dict["x"] == x_square and dict["y"] == y_square]
    return cell[0] if len(cell) > 0 else None

## Find in one definition cells a square with specific x and y values
def definition_by_x_and_y(x_square, y_square):
     cell = [dict for dict in ONE_DEFINITON_SQUARES if dict["x"] == x_square and dict["y"] == y_square]
     return cell[0] if len(cell) > 0 else None


def item_in_json_result(x, y, json_result):
    for line in json_result:
        if line["x"] == x and line["y"] == y:
            return True
    return False

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
    # Square x has negative slope because in Hebrew
    # you write from right to left and x axis is left to right.
    squareX = Linearline(-COLS, width, start_x, COLS)
    squareY = Linearline(ROWS, height, start_y, 0)

    # Change to squares instead of actual x and y pixels
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

        one_definition_cell = definition_by_x_and_y(x_square, y_square)
        two_definition_cell = double_definition_by_x_and_y(x_square, y_square)

        # One definition in specific cell
        if one_definition_cell is not None:

            # We need to "smash" the two dimesional text into one dimension

            flat_lines = [item for sublist in lines for item in sublist]
            new_text = [single_word["description"] for single_word in flat_lines]
            all_text = reduce(lambda row, word: row + " " + word, new_text)

            json_result.append({
                "x": x_square,
                "y": y_square,
                "text": [all_text.encode("utf-8")],
                "start_loc_x": one_definition_cell["start_loc_x"],
                "start_loc_y": one_definition_cell["start_loc_y"],
                "dir": one_definition_cell["dir"],
                "length": one_definition_cell["length"]
            })

        elif two_definition_cell is not None:

            two_definitions = []
            find_two_definitions_cells_result = findTwoDefinitionCells(lines)
            found_two_definitions = len(find_two_definitions_cells_result) > 1

            for block in find_two_definitions_cells_result:

                # We need to "smash" the two dimesional text into one dimension
                if len(block) != 1:
                    flat_lines = [item for sublist in block for item in sublist]
                elif isinstance(block, list) or isinstance(block, tuple):
                    flat_lines = block if isinstance(block[0], dict) else block[0]

                new_text = [single_word["description"] for single_word in flat_lines]
                all_text = reduce(lambda row, word: row + " " + word, new_text)

                two_definitions.append(all_text.encode("utf-8"))

            json_result.append({
                "x": x_square,
                "y": y_square,
                "text": two_definitions if found_two_definitions else two_definitions + [UNRESOLVED_TEXT],
                "length_left": two_definition_cell["length_left"],
                "length_down": two_definition_cell["length_down"]
            })



            ##Make sure to send "empty" definitions
    for cell in ONE_DEFINITON_SQUARES:
        if not item_in_json_result(cell["x"], cell["y"], json_result):
            cell_to_insert = cell.copy()
            cell_to_insert["text"] = [UNRESOLVED_TEXT]
            json_result.append(cell_to_insert)

    for cell in DOUBLE_DEFINITION_SQUARES:
        cell_to_insert = cell.copy()
        cell_to_insert["text"] = [UNRESOLVED_TEXT, UNRESOLVED_TEXT]
        json_result.append(cell_to_insert)






    return json_result

