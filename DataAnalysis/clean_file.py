"""
This script takes in a file containing gesture data and cleans it up by removing trials that have been striked out. 
The user should only utilize the UpdateFile() as the other ones are used as helpers for that method.

It requires pandas, os, and math to be installed in the environment.

This tool accepts .csv files and assumes that the file will have an x_counter and gesture_counter_UI column for analytics.

This script contains the following methods:
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



def clean_file(file):
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

    newDF = pd.DataFrame(data=None, columns = file.columns, index=file.index)
    newDF = newDF[0:0]
    testDF = file.copy()
    ui_counter = -1
    
    while (testDF.empty == False):
        #Gets the gesture_counter_UI of the first row in testDF
        gui_group_num = (testDF.iloc[0]["gesture_counter_UI"]).astype(int)                
        ui_counter += 1                                                  
        if (gui_group_num == ui_counter):              
            # Iterates through testDF and adds row from testDf to newDF and removes that row from testDF
            # until a new gesture has been recorded or a strike occurs                    
            for i in range(len(testDF.index)):
                if testDF.iloc[0]["gesture_counter_UI"] == ui_counter:                 
                    row = testDF.iloc[0].copy()
                    newDF.loc[len(newDF.index)] = row
                    testDF = testDF.iloc[1:]
                else:
                    # Unique exception in data file when there is data in the last row is nAN
                    # Ex) Sub10/Freeform_Sub10_Sess1/session_F_PanUp_subjID_10_05-10-23_02-37-19.csv
                    if (math.isnan(testDF.iloc[0]["gesture_counter_UI"])):
                        testDF = testDF.iloc[1:].dropna(how='all')
                    break
        else:                                                           
            # A strike has occured
            # Removes the most recent trial from newDF, which is the rows at the tail with the same gesture_counter_UI number
            if (newDF.empty == True):
                continue
            ui_counter -= 3
            tail_group_num = (newDF.iloc[-1]["gesture_counter_UI"])
            newDF.drop(newDF[newDF["gesture_counter_UI"] == tail_group_num].index, inplace = True)
            newDF.reset_index(drop=True, inplace=True)
            
    return newDF
    

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
    gesture_file_path = folder_path + "\\" + new_file_name
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

    ogFile = read_file(file_path)
    file_name = os.path.basename(file_path)
    gestureFilePath = get_file_export_path(file_name, folder_path)
    if not os.path.exists(gestureFilePath):
        if get_num_strikes(ogFile) > 0:
            cleanedFile = clean_file(ogFile)
            export_to_csv(cleanedFile, file_name, folder_path)
        else:
            export_to_csv(ogFile, file_name, folder_path)
