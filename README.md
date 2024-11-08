# Gesture Interface


## Table of Contents
1) Project Overview
2) Getting Started
3) File Descriptions & Dependencies


## File Descriptions & Dependencies

### `clean_file.py`

**Purpose**: Contains functions to help clean data files more efficiently and organized. Overall, it takes in a data file and removes trials that have been striked (when the x button is pressed and the x_counter increases).

- **Dependencies**: N/A

- **Connections**: 
  - Called by `export_clean_files.py` to get preprocessed data.


### `export_clean_files.py`

**Purpose**: Cleans data files by removing trials that have been striked and exports the new csv files to a specified CleanedData folder.

- **Dependencies**:
    - Requires a data directory as input.

- **Connections**: 
  - Not call on by any script but other scripts will require files outputted by this.
    - all_graph_vis.ipynb
    - metric_calculations.ipynb


### `all_graph_vis.ipynb`

**Purpose**: Visualizes participants' hand motion data. It outputs two different html files. The first is an individual figure of all of the trials in a single participant session. The second groups all of the individual single participant sessions for a single gesture on one file to view all simultaneously.

- **Dependencies**:
    - Requires a data directory as input. Data directory must be outputted from export_clean_files.py.
    - Requires a folder called "Figures" to output html visualizations to.

- **Connections**: 
    - Uses output files generated from export_clean_files.py as input.


### `metric_calculations.ipynb

**Purpose**: Performs metric calculations for specified features of the participants' gesture data. It then outputs the measurement value calculated for each of the first five trials per hand and exports it as csv file. For each gesture, there will be two files for freeform and instructional. 

- **Methodology**:
    - Remove accidental strokes based on strokes_to_remove csv files.
    - Run code six times for each of the metric calculations and edit variables accordingly.
    - Length
        - Use a sliding window of size 2 to calculate the distance between each pair and sum up all the lengths.
    - Duration
        - The time at which the trigger was released subtracted by the time at which the trigger was pulled.
    - Speed
        - Length / Duration: Uses the output files from the length and duration calculations.
    - Acceleration
        - Speed / Duration: Uses the output files from the speed and duration calculations.
    - Angle
        - Smooth the curve of the stroke using B-spline.
        - Determine 10 points on the curve.
        - Measure the external angle between two vectors made from every overlapping set of three consecutive points on the curve (dot product of two normalized vectors and the converted from radians to degrees).
        - Identify outliers with median absolute deviation and remove them from the list of curvature.
        - Calculate the average with the remaining values.
    - Curvature
        - Smooth the curve of the stroke using B-spline.
        - Determine 10 points on the curve.
        - Measure the curvature between every overlapping set of three consecutive points on the curve.
            - Find the triangle area created by the three data points 
                - Cross product of vectors 'ab' and 'bc' and calculate the norm from the result
                - Multiply it by .5
            - Use the menger curvature formula to calculate the curvature
                - (4 * area) / (ab * bc * ac)
                    - ab, bc, ac represents the length of each side on the triangle
        - Identify outliers with median absolute deviation and remove them from the list of curvature
        - Calculate the average with the remaining values.

- **Dependencies**:
    - Requires stroke removal csv file, which contains a list of strokes that were created on accident for each participant session.
    - Requires a data directory as input. Data directory must be outputted from export_clean_files.py
    - Requires a folder called "MetricCalculations" and subfolders for each of the metrics in there to output files to.

- **Connections**: 
    - Uses output files generated from export_clean_files.py as input.


### `metric_box_plots.py`

**Purpose**: Creates box plots based on the metric calculations data files.

- **Dependencies**:
    - Requires a data directory as input. Data directory must be outputted from export_clean_files.py.
    - Requires a subfolder in Figures called "BoxPlots" to output html visualizations to.

- **Connections**: 
    - Uses output files generated from metric_calculations.ipynb as input.


### `data_summary.py`

**Purpose**: Summarizes the metric calculations of each gesture session such as max, min, mean, etc.

- **Dependencies**:
    - Requires a data directory as input. Data directory must be outputted from metric_calculations.ipynb.
    - Requires a subfolder in MetricCalculations called "MetricSummary" to output summary files for each gesture to.

- **Connections**: 
    - Uses output files generated from metric_calculations.ipynb as input.


### `cb_info_extract.py`

**Purpose**: Analyzes codebook for all gestures and outputs a summary csv. Determines the percentage of participant sessions that create a certain shape for each hand, uses unimanual/bimanual, same/diff direction, and symmetry/asymmetry.

- **Dependencies**:
    - Requires a data directory as input. Data directory must be a folder called "Codebook" and contain codebook csvs for each gesture.

- **Connections**: 
    - N/A
