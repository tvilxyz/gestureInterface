"""
Overview
---------
This script is designed to generate box plots for gesture metrics from CSV files. Each CSV file corresponds to a gesture and contains data for left and right hand movements. The script exports these visualizations as HTML files, with each gesture type generating its own box plot.

Key Variables
-------------
    * metric_name (str): The name of the metric being visualized (e.g., "Duration").
    * unit_of_measurement (str): The unit of the metric (e.g., "Seconds").
    * input_folder (str): Path to the folder containing the input CSV files with gesture data.
    * output_folder (str): Path to the folder where generated box plot HTML files are saved.

Requirements
------
    * Edit the key variables
    * Repeat 6 times for the 6 different metrics, changing the metric_name, unit_of_measurement, and input_folder each time.
"""


import os
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np



'''Edit variables here'''
metric_name = "Duration"
unit_of_measurement = "Seconds"
#input_folder = "..\\gestureInterface\\MetricCalculations\\GestureDuration"
input_folder = os.path.join('..', 'gestureInterface', 'MetricCalculations', 'GestureDuration')
#output_folder = "..\\gestureInterface\\Figures\\BoxPlots"
output_folder = os.path.join('..', 'gestureInterface', 'Figures', 'BoxPlots')




def get_gesture_name(file_name):
    """
    Gets gesture name from file name.

    Parameters
    -----
        file_name : str
            name of file that was produced from the metric calculations. Has the format metric_for_gesture.csv
    
    Returns
    -----
        name_parts : list
            list of words that make up the file name
    """
    name_parts = file_name.split('_')
    return name_parts[2:]



def adjust_yaxis_to_whiskers(fig):
    """
    Autoscales each file to the min and max y based on boxplot traces.

    Parameters
    -----
        fig : go.Figure
            figure containing boxplot traces
    """

    whisker_max = float('-inf')

    # Loop through each trace in the figure to get whisker values
    for trace in fig.data:
        q1 = np.percentile(trace.y, 25)
        q3 = np.percentile(trace.y, 75)
        iqr = q3 - q1
        current_max = q3 + 1.5 * iqr

        whisker_max = max(whisker_max, current_max)

    # Update the y-axis range to match the whisker min/max
    fig.update_layout(yaxis=dict(range=[0, whisker_max]))



def export_boxplots(fig, gesture):
    """
    Exports boxplot traces to an html file.

    Parameters
    -----
        fig : go.Figure
            Figure containing boxplot traces
        gesture : str
            Name of the gesture being exported (Pan, Rot, or Zoom)
    """

    # Removes data points
    fig.update_traces(marker=dict(opacity=0))

    # Autoscale based on boxplot max
    adjust_yaxis_to_whiskers(fig)

    export_path = os.path.join(output_folder, 'Box_Plot_' + metric_name + '_' + gesture + '.html')
    if not os.path.exists(export_path):
        fig.write_html(export_path)



def generate_box_plots():
    """
    Takes a directory containing metric calculation values and generates boxplots.
    """

    # Initialize first boxplot
    curr_gesture = "Pan"
    fig = go.Figure()
    fig.update_layout(
        title=f"{metric_name}: {curr_gesture}",
        xaxis_title="Gestures (w/ Hand)",
        yaxis_title=unit_of_measurement,
    )

    # Colors for boxplot traces
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    color_index = 0

    files = sorted(os.listdir(input_folder))
    for file in files:
        df = pd.read_csv(os.path.join(input_folder, file)) 
        gesture_name = get_gesture_name(file)

        # Skip instructional files
        if gesture_name[-1] == "instructional.csv":
            continue

        # Move to the next gesture if the current gesture is different
        new_gesture = gesture_name[0].title()
        if curr_gesture.lower() != new_gesture.lower():
            export_boxplots(fig, curr_gesture)
            
            # Reset for the new gesture
            color_index = 0
            curr_gesture = new_gesture
            fig = go.Figure()
            fig.update_layout(
                title=f"{metric_name}: {curr_gesture}",
                xaxis_title="Gestures (w/ Hand)",
                yaxis_title=unit_of_measurement,
                yaxis=dict(range=[None, None])
            )

        # Drop the first row (header) and NaN values, then reset index
        df = df.iloc[1:].dropna().reset_index(drop=True)

        # Convert columns into lists for left and right gestures
        left_list = df.iloc[:, 0].tolist()
        if metric_name != "Duration":
            right_list = df.iloc[:, 1].tolist()

        # Add traces for left and right hand
        gesture_label = ' '.join(gesture_name[:-1]).title()
        if metric_name == "Duration":
            fig.add_trace(go.Box(y=left_list, name=f"{gesture_label}", marker_color=colors[color_index % len(colors)]))
        else:
            fig.add_trace(go.Box(y=left_list, name=f"{gesture_label} (L)", marker_color=colors[color_index % len(colors)]))
            fig.add_trace(go.Box(y=right_list, name=f"{gesture_label} (R)", marker_color=colors[color_index % len(colors)]))
            
        color_index += 1

    # Final plot export after loop finishes
    export_boxplots(fig, curr_gesture)

        
generate_box_plots()