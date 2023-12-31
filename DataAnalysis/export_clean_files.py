"""
This script utilizes a Data and CleanedData directory. It will iterate through a data directory, cleaning the data files within
the create, while creating subfolders within the clean data directory and exporting those clean files to their respective paths.

It assumes that there are two existing directories, a Data and CleanedData directory. Within the Data directory, there will 
be two subFolders, Sub# and SessionFolder sequentially, which represents the subject's identification number and all of their
sessions. The SessionFolder will contain files with all of the gesture data for that specific session. A sample path will 
have the format of ..\VRelax\gestureInterface\Data\Sub#\SessionFolder\GestureDataFile where Sub# will be replaced with the 
subject's number. SessionFolder and GestureDataFile can be any name but GestureDataFile must be a .csv

The program requires os.path to be downloaded into the environment and utilizes the clean_file.py file. 
"""

# import necessary packages
import warnings
warnings.filterwarnings('ignore')

import os.path 
from clean_file import *


# Relative paths to the Data and CleanedData folders
dataFolderPath = "..\\VRelax\\gestureInterface\\Data"
cleanDataFolderPath = "..\\VRelax\\gestureInterface\\CleanedData"

# List of paths to all of the subjectNumber folders - Sub1/Sub2/Sub3/etc
subjectNumberFolders = [f.path for f in os.scandir(dataFolderPath) if f.is_dir()] 

for subjectNumber in range(len(subjectNumberFolders)):
    # Checks for an existing subNum folder for each subject in the CleanData directory and creates one if there isn't one
    subjectNumberInCleanDataFolderPath = cleanDataFolderPath + "\\Sub" + str(subjectNumber+1)
    currSubNumPath = dataFolderPath + "\\Sub" + str(subjectNumber+1)
    if not os.path.exists(subjectNumberInCleanDataFolderPath):
        os.makedirs(subjectNumberInCleanDataFolderPath)

    # List of paths for all of the session folders for the single subNum folder
    currentSubjectNumberFolder = [f.path for f in os.scandir(currSubNumPath) if f.is_dir()]       

    # Iterates through the session folders in that subNum folder
    for sessionNumber in range(len(currentSubjectNumberFolder)):                      
        
        # Gets the current session folder path
        currentSessionFolderPath = currentSubjectNumberFolder[sessionNumber]  

        # Checks for an existing session folder in the CleanedData\SubNum path and creates one if there isn't
        sessionNumberInCleanDataFolderPath = subjectNumberInCleanDataFolderPath + "\\" + os.path.basename(currentSessionFolderPath)
        if not os.path.exists(sessionNumberInCleanDataFolderPath):
            os.makedirs(sessionNumberInCleanDataFolderPath)

        #iterates through all of the files in the session folder
        for fileNum in range(len(os.listdir(currentSessionFolderPath))):
            currentGestureFileName = (os.listdir(currentSessionFolderPath)[fileNum])
            currentGestureFilePath = currentSessionFolderPath + "\\" + currentGestureFileName
            GetUpdatedFile(currentGestureFilePath, sessionNumberInCleanDataFolderPath)
    
