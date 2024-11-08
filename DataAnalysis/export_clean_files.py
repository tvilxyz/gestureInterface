"""
Overview
------
This script utilizes a Data and CleanedData directory. It will iterate through a data directory, cleaning the data files within
the create, while creating subfolders within the clean data directory and exporting those clean files to their respective paths.

Key Variables
-------
    * data_folder_path (str): path to input data. Must have the format of ..\Data\Sub#\SessionFolder\GestureDataFile
    * clean_data_folder_path (str): empty folder to output clean data to. Folder must be called ..\CleanedData

Requirements
------- 
    * Edit variables: data_folder_path, clean_data_folder_path
"""

# import necessary packages
import warnings
warnings.filterwarnings('ignore')

import os.path 
from clean_file import *


# Relative paths to the Data and CleanedData folders
data_folder_path = "..\\VRelax\\gestureInterface\\Data"
clean_data_folder_path = "..\\VRelax\\gestureInterface\\CleanedData"

# List of paths to all of the subjectNumber folders - Sub1/Sub2/Sub3/etc
subject_number_folders = [f.path for f in os.scandir(data_folder_path) if f.is_dir()] 

for subject_number in range(len(subject_number_folders)):
    # Checks for an existing subNum folder for each subject in the CleanData directory and creates one if there isn't one
    subject_number_in_clean_data_folder_path = os.path.join(clean_data_folder_path, "Sub" + str(subject_number + 1))
    curr_sub_num_path = os.path.join(data_folder_path, "Sub" + str(subject_number + 1))
    if not os.path.exists(subject_number_in_clean_data_folder_path):
        os.makedirs(subject_number_in_clean_data_folder_path)

    # List of paths for all of the session folders for the single subNum folder
    curr_subject_number_folder = [f.path for f in os.scandir(curr_sub_num_path) if f.is_dir()]       

    # Iterates through the session folders in that subNum folder
    for sessionNumber in range(len(curr_subject_number_folder)):                      
        
        # Gets the current session folder path
        currentSessionFolderPath = curr_subject_number_folder[sessionNumber]  

        # Checks for an existing session folder in the CleanedData\SubNum path and creates one if there isn't
        sessionNumberInCleanDataFolderPath = os.path.join(subject_number_in_clean_data_folder_path, os.path.basename(currentSessionFolderPath))
        if not os.path.exists(sessionNumberInCleanDataFolderPath):
            os.makedirs(sessionNumberInCleanDataFolderPath)

        #iterates through all of the files in the session folder
        for fileNum in range(len(os.listdir(currentSessionFolderPath))):
            current_gesture_file_name = (os.listdir(currentSessionFolderPath)[fileNum])
            currentGestureFilePath = os.path.join(currentSessionFolderPath, current_gesture_file_name)
            get_updated_file(currentGestureFilePath, sessionNumberInCleanDataFolderPath)
    
