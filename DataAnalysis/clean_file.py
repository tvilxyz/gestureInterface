"""
Overview
------- 
This script takes in a file containing gesture data and cleans it up by removing trials that have been striked out. 
The user should only utilize the UpdateFile() as the other ones are used as helpers for that method.

Key Functions
------- 
    * clean_file - Removes trials that have been striked and returns a cleaned dataframe.
    * get_num_strikes - Gets the total number of strikes, or max x_counter, found in the file.
    * read_file - Converts a csv file into a dataframe.
    * export_to_csv - Converts the cleaned dataframe as a csv into a specified location.
    * get_updated_file - Reads, cleans, and exports a cleaned csv.
"""

import warnings
warnings.filterwarnings('ignore')

import os
import math
import pandas as pd



def clean_file(og_df):
    """
    Removes all of the gestures that have been striked out.
    An increase in the x_counter column, meaning the x button was pressed, removes the most recent trial.

    Iterates through testDF, a copy of the original dataframe, and adds that most recent trial for each gesture_counter_UI
    into newDF before removing it from testDF. Repeats until all rows have been analyzed, and testDF is empty.

    Parameters
    -----
    file : dataframe
        dataframe to clean

    Returns
    -----
    newDF : dataframe
        a new dataframe that represents the cleaned version of the original csv file
    """

    new_df = pd.DataFrame(columns = og_df.columns)

    total_gestures = int(og_df['gesture_counter'].max())
    strike_count = 0

    # Iterate through EVERY trial including 0 where the first trial has not yet begun
    for i in range(int(total_gestures)+1):
        # Add corresponding trial to new df
        new_df = pd.concat([new_df, og_df[og_df['gesture_counter'] == i]], ignore_index=True)
        # Check if strike count has gone up
        if strike_count < new_df['x_counter'].max():
            # If it has, remove the previous x trials from new df
            num_trials_to_remove = int(new_df['x_counter'].max() - strike_count)
            # Update strike count
            strike_count = new_df['x_counter'].max()
            for j in range(num_trials_to_remove):
                # Get the gesture counter of the last row and remove all rows with that value
                last_gesture_counter = new_df['gesture_counter'].iloc[-1]
                new_df = new_df[new_df['gesture_counter'] != last_gesture_counter]
    return new_df
    

def get_num_strikes(file):
    """
    Checks how many trials have been striked in the file.

    Parameters
    -----
    file : dataframe
        dataframe to clean

    Returns
    -----
    total_num_strikes : int
        the amount of strikes(x_counter) a file contains
    """

    total_num_strikes = file["x_counter"].max()
    return total_num_strikes


def read_file(file_path):
    """
    Reads a csv file based on the path and returns a new dataframe.

    Parameters
    -----
    file_path : string
        path to the csv file that needs to be cleaned
    
    Returns
    -----
    file : dataframe
        dataframe for the input csv file
    """

    file = pd.read_csv(file_path)
    return file

def get_file_export_path(file_name, folder_path):
    """
    Gets the path where the clean gesture data file will be exported to.

    Parameters
    ------
    file_name : string
        name of the original file
    folder_path : string
        path to the folder that the new csv will be exported to

    Returns
    -----
    gesture_file_path : string
        the path to the new gesture data file
    """

    new_file_name = "cleaned_" + file_name
    gesture_file_path = os.path.join(folder_path, new_file_name)
    return gesture_file_path

def export_to_csv(df, file_name, folder_path):
    """ 
    Exports a cleaned version of the csv file to a designated folder path.

    Parameters
    -----
    df : dataframe
        dataframe to clean
    file_name : string
        name of the csv file that was cleaned
    folder_path : string
        path to the folder that the new csv will be exported to
    """

    gesture_file_path = get_file_export_path(file_name, folder_path)
    if not os.path.exists(gesture_file_path):
        df.to_csv(gesture_file_path, header=True, index=False)


def get_updated_file(file_path, folder_path):
    """
    Takes in a csv file and returns a clean one.

    Parameters
    -----
    file_path : string
        path to the csv file that needs to be cleaned
    folder_path : string
        path to the export location of the clean csv file
    """

    og_file = read_file(file_path)
    file_name = os.path.basename(file_path)
    gestureFilePath = get_file_export_path(file_name, folder_path)
    
    if not os.path.exists(gestureFilePath):
        # If file contains strikes, clean it before exporting
        if get_num_strikes(og_file) > 0:
            cleanedFile = clean_file(og_file)
            export_to_csv(cleanedFile, file_name, folder_path)
        else:
            export_to_csv(og_file, file_name, folder_path)
