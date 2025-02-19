"""
Overview
------- 
This script takes in a metric calculation data file, summarizes the data, and exports two summary csv files for freeform and instructional. 
The summary contains the name, minimum, maximum, mean, median, std, sum, and difference between the min and max for each gesture.

Key Functions
------- 
    * create_columns - Adds descriptive static columns into an empty dataframe.
    * add_to_df - Gets the summary from the data df and adds it as a row to the total summarized dataframe.
    * add_sum_to_df - Creates columns for the sum of the left and right controller for min, max, and mean.
    * get_export_path - Gets the export path for the new summary file.
    * read_file - Converts a csv file into a dataframe.
    * summarize_data - Reads the original data file, summarizes it in a new csv, and exports it to a specified location.

Requirements
------- 
    * Edit variables: gesture
    * Run 6 times for the 6 different metrics, changing the gesture variable each time.
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


def add_to_df2(data_df, summary_df):
    for gesture in data_df:
        gesture_name = gesture

        # Must convert variable type. Floats are np.nan and tuples are string. 
        converted_vals = []
        for t in data_df[gesture]:
            if isinstance(t, str) == True:
                t = tuple(map(float, t.strip("()").split(",")))
            else:
                t = np.nan
            converted_vals.append(t)

        # Update the DataFrame column with the cleaned/converted values
        data_df[gesture] = converted_vals

        # Extract x, y, and z values from the tuples
        x_vals = [t[0] for t in data_df[gesture] if isinstance(t, tuple)]
        y_vals = [t[1] for t in data_df[gesture] if isinstance(t, tuple)]
        z_vals = [t[2] for t in data_df[gesture] if isinstance(t, tuple)]

        gesture_min = (min(x_vals), min(y_vals), min(z_vals))
        gesture_max = (max(x_vals), max(y_vals), max(z_vals))
        gesture_mean = (sum(x_vals) / len(x_vals), sum(y_vals) / len(y_vals), sum(z_vals) / len(z_vals))
        gesture_median = (
            sorted(x_vals)[len(x_vals) // 2],
            sorted(y_vals)[len(y_vals) // 2],
            sorted(z_vals)[len(z_vals) // 2]
        )
        gesture_std = (
            (sum((x - gesture_mean[0])**2 for x in x_vals) / len(x_vals))**0.5,
            (sum((y - gesture_mean[1])**2 for y in y_vals) / len(y_vals))**0.5,
            (sum((z - gesture_mean[2])**2 for z in z_vals) / len(z_vals))**0.5
        )
        gesture_sum = (sum(x_vals), sum(y_vals), sum(z_vals))
        gesture_diff = (
            gesture_max[0] - gesture_min[0],
            gesture_max[1] - gesture_min[1],
            gesture_max[2] - gesture_min[2]
        )

        summary_df.loc[gesture_name] = [gesture_name, gesture_min, gesture_max, gesture_mean, gesture_median, gesture_std, gesture_sum, gesture_diff]
        

def add_sum_to_df(summary_df):
    """
    Adds three new columns to the summary dataframe: sum of both hand controllers for .the min, max, and mean

    Parameters
    -----
    summary_df : dataframe
        data frame that will contain all the gesture summaries
    """

    sum_min, sum_max, sum_mean = 0, 0, 0

    min_list, max_list, mean_list = [], [], []

    for row_num in range(len(summary_df)):
        # If row is for left controller, the sum_min, sum_max, sum_mean will be replaced with the right controller data
        if row_num % 2 == 0:
            sum_min = summary_df.iloc[row_num]['min']
            sum_max = summary_df.iloc[row_num]['max']
            sum_mean = summary_df.iloc[row_num]['mean']
        # Row is for right controller
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


def add_sum_to_df2(summary_df):
    """
    Adds three new columns to the summary dataframe: sum of both hand controllers for .the min, max, and mean

    Parameters
    -----
    summary_df : dataframe
        data frame that will contain all the gesture summaries
    """

    sum_min, sum_max, sum_mean = (0,0,0), (0,0,0), (0,0,0)

    min_list, max_list, mean_list = [], [], []

    for row_num in range(len(summary_df)):
        # If row is for left controller, the sum_min, sum_max, sum_mean will be replaced with the right controller data
        if row_num % 2 == 0:
            sum_min = summary_df.iloc[row_num]['min']
            sum_max = summary_df.iloc[row_num]['max']
            sum_mean = summary_df.iloc[row_num]['mean']
        else:
            sum_min = (sum_min[0] + summary_df.iloc[row_num]['min'][0], 
                       sum_min[1] + summary_df.iloc[row_num]['min'][1],
                       sum_min[2] + summary_df.iloc[row_num]['min'][2])
            sum_max = (sum_max[0] + summary_df.iloc[row_num]['max'][0], 
                       sum_max[1] + summary_df.iloc[row_num]['max'][1],
                       sum_max[2] + summary_df.iloc[row_num]['max'][2])
            sum_mean = (sum_mean[0] + summary_df.iloc[row_num]['mean'][0], 
                       sum_mean[1] + summary_df.iloc[row_num]['mean'][1],
                       sum_mean[2] + summary_df.iloc[row_num]['mean'][2])
            min_list.append(sum_min)
            max_list.append(sum_max)
            mean_list.append(sum_mean)
            min_list.append(sum_min)
            max_list.append(sum_max)
            mean_list.append(sum_mean)

    summary_df.loc[:, 'L/R_sum_of_min'] = min_list
    summary_df.loc[:, 'L/R_sum_of_max'] = max_list
    summary_df.loc[:, 'L/R_sum_of_mean'] = mean_list


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

    folder_path_split = os.path.split(input_folder_path)
    metric_name = folder_path_split[-1][7:].lower()

    new_export_path = os.path.join(output_folder_path, f"{metric_name}_{sessiontype}_summary.csv")

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
    gesture_files_list = sorted(gesture_files_list)

    # Create summary df template with columns for both freeform and instructional
    freeform_summary_df = pd.DataFrame()
    instructional_summary_df = pd.DataFrame()
    create_columns(freeform_summary_df)
    create_columns(instructional_summary_df)

    # Gets the summary of each column in the files and adds it to the summary df depending on the session type
    for file_num in range(len(gesture_files_list)):
        data_df = read_file(os.path.join(input_folder_path, gesture_files_list[file_num]))
        if (file_num%2 == 0):
            if (gesture == "GestureVelocity") or (gesture == "GestureAcceleration"):
                add_to_df2(data_df, freeform_summary_df)
            else:
                add_to_df(data_df, freeform_summary_df)
        else:
            if (gesture == "GestureVelocity") or (gesture == "GestureAcceleration"):
                add_to_df2(data_df, instructional_summary_df)
            else:
                add_to_df(data_df, instructional_summary_df)
    

    if (gesture == "GestureVelocity") or (gesture == "GestureAcceleration"):
        add_sum_to_df2(freeform_summary_df)
        add_sum_to_df2(instructional_summary_df)
    else:
        add_sum_to_df(freeform_summary_df)
        add_sum_to_df(instructional_summary_df)

    # Exports new summary files to a specified folder
    freeform_export_path = get_export_path('freeform', output_folder_path, input_folder_path)
    instructional_export_path = get_export_path('instructional', output_folder_path, input_folder_path)

    
    if not os.path.exists(freeform_export_path):
        freeform_summary_df.to_csv(freeform_export_path, header=True, index=False)
    if not os.path.exists(instructional_export_path):
        instructional_summary_df.to_csv(instructional_export_path, header=True, index=False)
    

        
'''Edit variable here'''
# Folder name for metric data
gesture = "GestureAcceleration"

# Folder containing data from a single gestire in metric calculations. Must run 6 times for the 6 different metrics with the new paths.
input_folder_path = os.path.join('..', 'MetricCalculations', gesture)

# Folder where files will be outputted to
export_folder_path = os.path.join('..', 'MetricCalculations', "MetricSummary")

summarize_data(export_folder_path, input_folder_path)