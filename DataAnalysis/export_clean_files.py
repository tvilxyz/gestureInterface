"""
Overview
------
This script utilizes a Data and CleanedData directory. It will iterate through a data directory, cleaning the data files within
the create, while creating subfolders within the clean data directory and exporting those clean files to their respective paths.

Key Variables
-------
    * data_folder_path (str): path to input data. Must have the format of ..\Data\Sub#\SessionFolder\GestureDataFile
    * clean_data_folder_path (str): empty folder to output clean data to. Folder must be called ..\CleanedData
"""

# import necessary packages
import warnings
warnings.filterwarnings('ignore')

import os.path 
from clean_file import *


# Relative paths to the Data and CleanedData folders
data_folder_path = os.path.join('..', 'Data')
clean_data_folder_path = os.path.join('..', 'CleanedData')

# List of paths to all of the subjectNumber folders - Sub01/Sub02/Sub03/etc
sub_folders_in_data = [f.path for f in os.scandir(data_folder_path) if f.is_dir()] 

for sub_folder in sub_folders_in_data:
    
    # Checks for an existing subNum folder for each subject in the CleanData directory and creates one if there isn't one
    sub_num_in_clean_data_path = os.path.join(clean_data_folder_path, os.path.basename(sub_folder))

    if not os.path.exists(sub_num_in_clean_data_path):
        os.makedirs(sub_num_in_clean_data_path)

    # List of paths for all of the session folders in Data/SubNum
    curr_subject_number_folder = [f.path for f in os.scandir(sub_folder) if f.is_dir()]       

    # Iterates through the session folders in Data/SubNum folder
    for session_folder in curr_subject_number_folder:                      

        # Checks for an existing session folder in the CleanedData\SubNum path and creates one if there isn't
        session_folder_path = os.path.join(sub_num_in_clean_data_path, os.path.basename(session_folder))

        if not os.path.exists(session_folder_path):
            os.makedirs(session_folder_path)

        # Iterates through all of the files in the session folder
        for fileNum in range(len(os.listdir(session_folder))):
            current_gesture_file_name = (os.listdir(session_folder)[fileNum])
            currentGestureFilePath = os.path.join(session_folder, current_gesture_file_name)
            get_updated_file(currentGestureFilePath, session_folder_path)