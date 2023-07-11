# import necessary packages
import warnings
warnings.filterwarnings('ignore')

import csv
import pandas as pd
import numpy as np
from plotnine import *
import statsmodels.api as sm

from sklearn.linear_model import LinearRegression # Linear Regression Model
from sklearn.preprocessing import StandardScaler # Z-score variables
from sklearn.preprocessing import MinMaxScaler # Min-Max Normalization

from sklearn.model_selection import train_test_split # simple TT split cv

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def CleanFile(inputDF):
    newDF = pd.DataFrame(data=None, columns = inputDF.columns, index=inputDF.index)
    newDF = newDF[0:0]
    tempDF = inputDF.copy()
    uiCounter = -1                              #uiCounter keeps track of what the gestureCounterUI should be if things run smoothly
    
    while (tempDF.empty == False):
        guiGroupNum = (tempDF.iloc[0]["gesture_counter_UI"]).astype(int)                
        uiCounter += 1                                                  
        #Subject has started a new gesture successfully
        #Adds the rows with the same gestureCounterUI and stops when the next row has a different number
        #This could mean that a new gesture has started or the x was pressed.
        if (guiGroupNum == uiCounter):                                  
            for i in range(len(tempDF.index)):
                if tempDF.iloc[0]["gesture_counter_UI"] == uiCounter:                 
                    row = tempDF.iloc[0].copy()
                    newDF.loc[len(newDF.index)] = row
                    tempDF = tempDF.iloc[1:]
                else:
                    break
        #x counter was pressed
        #gets the gestureCounterUI of the last row in the newDF and deletes all of the rows with the same gestureCounterUI
        else:                                                           
            uiCounter -= 3
            tailGroupNum = (newDF.iloc[-1]["gesture_counter_UI"])
            newDF.drop(newDF[newDF["gesture_counter_UI"] == tailGroupNum].index, inplace = True)
            newDF.reset_index(drop=True, inplace=True)
    return newDF
    
#Gets the number of strikes found in the file
def GetNumStrikes(inputDF):
    totalNumStrikes = inputDF["x_counter"].max()
    return totalNumStrikes

def ReadFile(fileName):
    inputDF = pd.read_csv(fileName)
    return inputDF

def ExportToCSV(dataFrame, fileName):
    path = 'C:\\Users\\Documents\\CPSC_Courses\\Personal\\VRelax\\gestureInterface\\CleanData'
    newFileName = "cleaned_" + fileName
    dataFrame.to_csv(newFileName, header=True, index=False)

#Detects strikes in inputFile
#Exports an new clean csv if strikes are found and returns the inputFile if no strikes are found
def GetUpdatedFile(fileName):
    inputDF = ReadFile(fileName)
    if GetNumStrikes(inputDF) > 0:
        cleanedDF = CleanFile(inputDF)
        ExportToCSV(cleanedDF, fileName)
    else:
        ExportToCSV(inputDF, fileName)

GetUpdatedFile("session_I_PanLeft_subjID_26_06-29-23_01-59-16.csv")