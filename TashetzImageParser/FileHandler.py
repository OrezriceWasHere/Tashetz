import os
from shutil import copy2


# Directories constants
GLOBAL_TASHETZ_DIRECTORY = os.path.join("F:\\", "Tashetz")
ANALYSIS_DIRECTORY = os.path.join(GLOBAL_TASHETZ_DIRECTORY, "Analysis")
ANALYSIS_TEXT_FILE = "analysis.txt"
GOOGLE_TEXT_FILE = "google.txt"



# Images global
LIST_IMAGES = filter(lambda dir: dir.startswith("IMG"), os.listdir(GLOBAL_TASHETZ_DIRECTORY))


# Creatae a directory regarding the analysis of an image.
# A new directory will be create under Tashetz global directory called "Analysis" (Very Original, huh?)
# And inside it a new directory will be created for each analysis of an image.
# The analysis contains (Meanwhile...) the original image, the goole API analysis,
# and parsing that analysis into squares
def Save_Analysis_Files_To_Directory(image, googleAnalysis, finalResult):



    # Create Analysis Folder
    if not os.path.exists(ANALYSIS_DIRECTORY):
        os.makedirs(ANALYSIS_DIRECTORY)

    print "saving results to " + ANALYSIS_DIRECTORY + " ..."

    # Create the unique folder for the image
    image_name, image_extension = os.path.splitext(image)
    image_analysis_directory = os.path.join(ANALYSIS_DIRECTORY, image_name)
    if not os.path.exists(image_analysis_directory):
        os.makedirs(image_analysis_directory)

    # Copy image into the new folder
    Copy_Image_To_Analysis_Directory(os.path.join(GLOBAL_TASHETZ_DIRECTORY, image),
                                     image_analysis_directory)

    # Copy google analysis to the new folder
    Copy_Google_To_Anaylysis_Directory(googleAnalysis, image_analysis_directory)

    # Copy software analysis to the new folder
    Copy_Final_Result_To_Analysis_Directory(finalResult, image_analysis_directory)

    print "done."

    pass

def Copy_Image_To_Analysis_Directory(imageLocation, directoryLocation):

    print "copying image " + imageLocation + " to " + directoryLocation + " ..."

    if not os.path.exists(os.path.join(directoryLocation, os.path.basename(imageLocation))):
        copy2(imageLocation, directoryLocation)

    print "done."

    pass

def Copy_Google_To_Anaylysis_Directory(googleAnaylsis, directoryLocation):

    print "saving google analysis to folder " + directoryLocation + " ..."

    CreateFile(googleAnaylsis, os.path.join(directoryLocation,  GOOGLE_TEXT_FILE))

    print "done."

    pass

def Copy_Final_Result_To_Analysis_Directory(finalResult, directoryLocation):

    print "saving local analysis to folder " + directoryLocation +  " ..."

    CreateFile(finalResult, os.path.join(directoryLocation, ANALYSIS_TEXT_FILE))

    print "done."
    pass

def CreateFile(text, directory):


    with open(directory, "w") as file:
        file.write(text)

def readFromFile(directory):

    with open(directory) as file:
        return file.read()

def verifyFilesIntegrity():
    if not os.path.isdir(GLOBAL_TASHETZ_DIRECTORY) or not LIST_IMAGES:
        print "Oh no! no tashetz directory in " + GLOBAL_TASHETZ_DIRECTORY + " or no image file (starts with 'IMG')! "
        print "It's such a disaster!"
        print "It's the biggest trouble so far"
        exit()
