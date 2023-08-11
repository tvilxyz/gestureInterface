"""
This script takes in a boxplot data file, summarizes the data, and exports the summary as a csv file. The summary contains the name, minimum, 
maximum, mean, median, std, sum, and difference between the min and max for each gesture.

The user should not modify any of the methods, but the two variables at the bottom of the program named data_file_path and export_folder_path 
should be changed to path of the file/folder on the user's computer. 

The export_folder_path variable can be any folder path the user would like the summary to be exported to, and the data_file_path must be a file
that has been successfully ran and created with the gesture_box_plot.ipynb file.

It requires pandas, os, and numpy to be installed in the environment.

This script contains the following methods:
    * create_columns - Adds descriptive static columns into an empty dataframe.
    * create_new_df - Creates a complete dataframe that represents a summary of the boxplot data files.
    * get_export_path - Gets the export path for the new summary file.
    * read_file - Converts a csv file into a dataframe.
    * summarize_data - Reads the original data file, summarizes it in a new csv, and exports it to a specified location.
"""

import os
import pandas as pd
import numpy as np

def read_file(file_path):
    """
    Reads a csv file into a dataframe.

    Parameters
    -----
    file_path : str
        path to a csv file

    Returns
    -----
    file : dataframe
        a dataframe of the input csv file
    """
    
    file = pd.read_csv(file_path)
    return file

def create_columns(df):
    """
    Create metric columns for the dataframe. Ex) minimum, maximum, mean, etc

    Parameters
    -----
    df : dataframe
        dataframe to add new columns to
    """
    df['gesture'] = np.nan
    df['min'] = np.nan
    df['max'] = np.nan
    df['mean'] = np.nan
    df['median'] = np.nan
    df['std'] = np.nan
    df['sum'] = np.nan
    df['difference'] = np.nan

def create_new_df(data_df):
    """
    Creates a dataframe that summarize a data file. Contains the min, max, mean, median, std, sum, and difference of each gesture.

    Parameters
    -----
    data_df : dataframe
        data frame to summarize

    Returns
    -----
    new_df : dataframe
        a summarized version of the original dataframe
    """

    new_df = pd.DataFrame()

    create_columns(new_df)
    
    for gesture in data_df:
        gesture_name = gesture
        gesture_min = data_df[gesture].min()
        gesture_max = data_df[gesture].max()
        gesture_mean = data_df[gesture].mean()
        gesture_median = data_df[gesture].median()
        gesture_std = data_df[gesture].std()
        gesture_sum = data_df[gesture].sum()
        gesture_diff = gesture_max - gesture_min

        new_df.loc[gesture_name] = [gesture_name, gesture_min, gesture_max, gesture_mean, gesture_median, gesture_std, gesture_sum, gesture_diff]

    return new_df

def get_export_path(output_folder_path, data_file_path):
    """
    Gets export path for the file.

    Parameters
    -----
    output_folder_path : str
        path to the folder it will be exported to
    data_file_path : str
        path to the original data file to get the metric's name

    Returns
    -----
    export_path : str
        the summarized data file's path
    """
    export_path = output_folder_path
    name_split = os.path.basename(data_file_path).split('_')
    metric_name = name_split[2]
    export_path += '\\' + metric_name + '_summary.csv'

    return export_path

def summarize_data(output_folder_path, data_file_path):
    """
    Creates a summarized data file for the box plot data and exports it to a specified path.

    Parameters
    -----
    output_folder_path : str
        path to the folder it will be exported to
    data_file_path : str
        path to the original data file to get the metric's name
    """

    data_df = read_file(data_file_path)

    # Create summarized dataframe
    summarized_df = create_new_df(data_df)

    # Get output path
    export_path = get_export_path(output_folder_path, data_file_path)

    # Export to csv if it the path does not exist
    if not os.path.exists(export_path):
        summarized_df.to_csv(export_path, header=True, index=False)


"""
Modify the two variables below to the path of the file and folder on the computer.

The export_folder_path variable can be any folder path the user would like the summary to be exported to, and the data_file_path must be a file
that has been successfully ran and created with the gesture_box_plot.ipynb file.
"""

data_file_path = 'C:\\Users\\vrelax\\Desktop\\VRelax\\gestureInterface\\BoxPlots\\GestureTime\\all_gestures_times_data.csv'
export_folder_path = 'C:\\Users\\vrelax\\Desktop\\VRelax\\gestureInterface\\BoxPlots\\MetricSummary'
summarize_data(export_folder_path, data_file_path)