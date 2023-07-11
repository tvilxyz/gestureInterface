"""
This script takes in a file containing gesture data and cleans it up by removing trials that have been striked out. 
The user should only utilize the UpdateFile() as the other ones are used as helpers for that method.

It requires pandas, os, and math to be installed in the environment.

This tool accepts .csv files and assumes that the file will have an x_counter and gesture_counter_UI column for analytics.

This script contains the following methods:
    * CleanFile - Removes trials that have been striked and returns a cleaned dataframe.
    * GetNumStrikes - Gets the total number of strikes, or max x_counter, found in the file.
    * ReadFile - Converts a csv file into a dataframe.
    * ExportToCSV - Converts the cleaned dataframe as a csv into a specified location.
    * GetUpdatedFile - Reads, cleans, and exports a cleaned csv.
"""

import warnings
warnings.filterwarnings('ignore')

import os
import math
import pandas as pd



def CleanFile(file):
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
    uiCounter = -1
    
    while (testDF.empty == False):
        #Gets the gesture_counter_UI of the first row in testDF
        guiGroupNum = (testDF.iloc[0]["gesture_counter_UI"]).astype(int)                
        uiCounter += 1                                                  
        if (guiGroupNum == uiCounter):              
            # Iterates through testDF and adds row from testDf to newDF and removes that row from testDF
            # until a new gesture has been recorded or a strike occurs                    
            for i in range(len(testDF.index)):
                if testDF.iloc[0]["gesture_counter_UI"] == uiCounter:                 
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
            uiCounter -= 3
            tailGroupNum = (newDF.iloc[-1]["gesture_counter_UI"])
            newDF.drop(newDF[newDF["gesture_counter_UI"] == tailGroupNum].index, inplace = True)
            newDF.reset_index(drop=True, inplace=True)
            
    return newDF
    

def GetNumStrikes(file):
    """
    Checks how many trials have been striked in the file.

    Parameters
    -----
    file : dataframe
        dataframe to clean

    Returns
    -----
    totalNumStrikes : int
        the amount of strikes(x_counter) a file contains
    """

    totalNumStrikes = file["x_counter"].max()
    return totalNumStrikes


def ReadFile(filePath):
    """
    Reads a csv file based on the path and returns a new dataframe.

    Parameters
    -----
    filePath : str
        path to the csv file that needs to be cleaned
    
    Returns
    -----
    file : dataframe
        dataframe for the input csv file
    """

    file = pd.read_csv(filePath)
    return file

def GetFileExportPath(fileName, folderPath):
    """
    Gets the path where the clean gesture data file will be exported to.

    Parameters
    ------
    fileName : string
        name of the original file
    folderPath : string
        path to the folder that the new csv will be exported to

    Returns
    -----
    gestureFilePath : string
        the path to the new gesture data file
    """

    newFileName = "cleaned_" + fileName
    gestureFilePath = folderPath + "\\" + newFileName
    return gestureFilePath

def ExportToCSV(dataFrame, fileName, folderPath):
    """ 
    Exports a cleaned version of the csv file to a designated folder path.

    Parameters
    -----
    dataframe : dataframe
        dataframe to clean
    fileName : string
        name of the csv file that was cleaned
    folderPath : string
        path to the folder that the new csv will be exported to
    """

    gestureFilePath = GetFileExportPath(fileName, folderPath)
    if not os.path.exists(gestureFilePath):
        dataFrame.to_csv(gestureFilePath, header=True, index=False)


def GetUpdatedFile(filePath, folderPath):
    """
    Takes in a csv file and returns a clean one.

    Parameters
    -----
    filePath : str
        path to the csv file that needs to be cleaned
    folderPath : string
        path to the export location of the clean csv file
    """

    ogFile = ReadFile(filePath)
    fileName = os.path.basename(filePath)
    gestureFilePath = GetFileExportPath(fileName, folderPath)
    if not os.path.exists(gestureFilePath):
        if GetNumStrikes(ogFile) > 0:
            cleanedFile = CleanFile(ogFile)
            ExportToCSV(cleanedFile, fileName, folderPath)
        else:
            ExportToCSV(ogFile, fileName, folderPath)
