# Gesture Interface

## Please make the following folders:
- Cleaned Data
- Data
- Figures
- AllData (eacxh of the folders under AllData will have the 37 corresponding csv gesture data)
    - F_BoxSelect
    - F_PanDown
    - F_PanLeft
    - F_PanRight
    - F_PanUp
    - F_RotBackX
    - F_RotClockwiseY
    - F_RotCounterY
    - F_RotForwardX
    - F_RotLeftZ
    - F_ZoomIn
    - F_ZoomOut
    - I_BoxSelect
    - I_PanDown
    - I_PanLeft
    - I_PanRight
    - I_PanUp
    - I_RotBackX
    - I_RotClockwiseY
    - I_RotCounterY
    - I_RotForwardX
    - I_RotLeftZ
    - I_ZoomIn
    - I_ZoomOut

## Important Scripts:
- all_graph_vis.ipynb
    - Overview: This script helps visualize all of the participants and their sessions' data in one figure. There are 26 participants and 37 3-dimensional graphs.
    - "data_folder" is the path you will modify depending on what gesture you would like to analyze. For example, in this case I wrote the relative path "../AllData/F_RotForwardX" since I wanted to analyze the Rotate Froward gesture for all of my participants.
    - Then, we will iterate through all of the data in the given folder.
    - For each csv (which represesents a session), we create a correspoding dataframe that removes any data points that are not triggered by either the left or right trigger, add the participant number as a column (denoted by participant_num), and add the unique session identifier as a column (denoted by session_identifier). All of these dataframes are concatenated into a single dataframe.
    - Afterwards, we group the dataframe by participant number and session identifier so we can display 37 figures in total.
    - Rows and columns are setermined by the sqrt of the number of participants.
    - We iterate over the grouped data by participant and session, and then iterate over each trial for each participant and session (which is denoted by gesture_counter) and add scatter traces
    - After looping through all 37 sessions, we save the figure in the given output file, which you can change using the "output_path"
