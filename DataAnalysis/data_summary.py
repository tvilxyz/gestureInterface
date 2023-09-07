"""
This script takes in a boxplot data file, summarizes the data, and exports two summary csv files for freeform and instructional. 
The summary contains the name, minimum, maximum, mean, median, std, sum, and difference between the min and max for each gesture.

The user should not modify any of the methods, but the two variables at the bottom of the program named input_folder_path and export_folder_path 
should be changed to path of the folders on the user's computer. 

The export_folder_path variable can be any folder path the user would like the summary to be exported to, and the input_folder_path must be a directory 
that contains the box plot data files which has been successfully ran and created with the gesture_box_plot.ipynb file.

It requires pandas, os, and numpy to be installed in the environment.

This script contains the following methods:
    * create_columns - Adds descriptive static columns into an empty dataframe.
    * add_to_df - Gets the summary from the data df and adds it as a row to the total summarized dataframe.
    * add_sum_to_df - Creates columns for the sum of the left and right controller for min, max, and mean.
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
    #df['L/R_sum_of_min'] = np.nan
    #df['L/R_sum_of_max'] = np.nan
    #df['L/R_sum_of_mean'] = np.nan


def add_to_df(data_df, summary_df):
    """
    Gets the summary from the data df and adds it as a row to the total summarized dataframe.

    Parameters
    -----
    data_df : dataframe
        data frame to summarize
    summary_df : dataframe
        data frame that will contain all the gesture summaries
    """

    row_num = 1
    sum_min = 0
    sum_max = 0
    sum_mean = 0

    for gesture in data_df:
        gesture_name = gesture
        gesture_min = data_df[gesture].min()
        gesture_max = data_df[gesture].max()
        gesture_mean = data_df[gesture].mean()
        gesture_median = data_df[gesture].median()
        gesture_std = data_df[gesture].std()
        gesture_sum = data_df[gesture].sum()
        gesture_diff = gesture_max - gesture_min

        summary_df.loc[gesture_name] = [gesture_name, gesture_min, gesture_max, gesture_mean, gesture_median, gesture_std, gesture_sum, gesture_diff]


def add_sum_to_df(summary_df):
    """
    Adds three new columns to the summary dataframe: sum of both hand controllers for .the min, max, and mean

    Parameters
    -----
    summary_df : dataframe
        data frame that will contain all the gesture summaries
    """

    sum_min = 0
    sum_max = 0
    sum_mean = 0

    min_list = []
    max_list = []
    mean_list = []

    for row_num in range(len(summary_df)):
        # If row is for left controller, the sum_min, sum_max, sum_mean will be replaced with the right controller data
        if row_num % 2 == 0:
            sum_min = summary_df.iloc[row_num]['min']
            sum_max = summary_df.iloc[row_num]['max']
            sum_mean = summary_df.iloc[row_num]['mean']
        else:
            sum_min += summary_df.iloc[row_num]['min']
            sum_max += summary_df.iloc[row_num]['max']
            sum_mean += summary_df.iloc[row_num]['mean']
            min_list.append(sum_min)
            max_list.append(sum_max)
            mean_list.append(sum_mean)
            min_list.append(sum_min)
            max_list.append(sum_max)
            mean_list.append(sum_mean)

    summary_df.loc[:, ['L/R_sum_of_min']] = min_list
    summary_df.loc[:, ['L/R_sum_of_max']] = max_list
    summary_df.loc[:, ['L/R_sum_of_mean']] = mean_list


def get_export_path(sessiontype, output_folder_path, input_folder_path):
    """
    Gets export path for the file.

    Parameters
    -----
    output_folder_path : str
        path to the folder it will be exported to
    input_folder_path : str
        path to the folder that contains the box plot data files

    Returns
    -----
    new_export_path : str
        the summarized data file's path
    """

    folder_path_split = input_folder_path.split('\\')
    metric_name = folder_path_split[-1][7:].lower()

    new_export_path = output_folder_path + '\\' + metric_name + '_' + sessiontype + '_summary.csv'
    return new_export_path


def summarize_data(output_folder_path, input_folder_path):
    """
    Creates a summarized data file for the box plot data and exports it to a specified path.

    Parameters
    -----
    output_folder_path : str
        path to the folder it will be exported to
    input_folder_path : str
        path to the folder that contains the box plot data files
    """

    # Get all data files in the input directory
    gesture_files_list = os.listdir(input_folder_path)

    # Create summary df template with columns for both freeform and instructional
    freeform_summary_df = pd.DataFrame()
    instructional_summary_df = pd.DataFrame()
    create_columns(freeform_summary_df)
    create_columns(instructional_summary_df)

    # Gets the summary of each column in the files and adds it to the summary df depending on the session type
    for file_num in range(len(gesture_files_list)):
        data_df = read_file(os.path.join(input_folder_path, gesture_files_list[file_num]))
        if (file_num%2 == 0):
            add_to_df(data_df, freeform_summary_df)
        else:
            add_to_df(data_df, instructional_summary_df)
    
    add_sum_to_df(freeform_summary_df)
    add_sum_to_df(instructional_summary_df)

    # Exports new summary files to a specified folder
    freeform_export_path = get_export_path('freeform', output_folder_path, input_folder_path)
    instructional_export_path = get_export_path('instructional', output_folder_path, input_folder_path)

    
    if not os.path.exists(freeform_export_path):
        freeform_summary_df.to_csv(freeform_export_path, header=True, index=False)
    if not os.path.exists(instructional_export_path):
        instructional_summary_df.to_csv(instructional_export_path, header=True, index=False)
    

        

    
"""
Modify the two variables below to the path of the file and folder on the computer.

The export_folder_path variable can be any folder path the user would like the summary to be exported to, and the import_folder_path which must 
be a folder that contains the data files from the metric calculations created in the gesture_box_plot.ipynb.
"""

input_folder_path = '..\\GestureLength'
export_folder_path = '..\\MetricSummary'
summarize_data(export_folder_path, input_folder_path)