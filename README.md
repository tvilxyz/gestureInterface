# Gesture Interface

## Please make the following folders:
- BoxPlots
- Cleaned Data
- Data (should follow a similar format below. more details in the export_clean_files documentation)
    - Sub1
        - Freeform_Sub1_Sess1
            - file.csv
        _ Instructional_Sub1_Sess1
            - file.csv
    - Sub2
    - ...
- Figures
- AllData (each of the folders under AllData will have the 37 corresponding csv gesture data)
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
- clean_file.py
    - Overview: This script provides methods to help clean data files more efficiently in an organized manner.
    - Only the get_updated_file(file_path, folder_path) should be used as the other methods are helpers.
    - The file takes in a csv file and reads it into a dataframe.
    - It first checks if there are any strikes in the file to see if it needs to be cleaned. If there isn't any, the original file is returned.
    - To clean the file, we look at the gesture_counter_ui to determine which rows will need to be removed in the new dataframe. Only the most recent gesture_counter_ui for each of the trial number should be kept.
    - An example of the above: If the original file had gesture_counter_UI rows [1,1,2,3,3,2,3,4], the new file should only have the rows [1,1,2,2,3,4]. The most recent trial number for 3 at index [6] is kept while the rows at index [3] and index [4] are removed.
    - To observe how the file works with more simple data, the ..\Documentation folder contains two test csv data files.
- export_clean_files.py
    - Overview: This script cleans data files using the clean_file.py and exports the new csv files to a CleanedData folder.
    - The file will iterate through the data folder, clean, and export each individual csv data files to its new path. The CleanData folder will have a similar tree as the Data folder. However, the file name will have a 'cleaned_' added prior its original file name as its new name.
    - Utilizes get_updated_file(file_path, folder_path) method from clean_file.py where filePath is the path to the csv data file and folderPath is the path to the folder that the new cleaned file should be exported to.
    - You will need need to modify the data_folder_path and clean_data_folder_path. clean_data_folder_path must have a folder called CleanedData but can be empty. data_folder_path is expected to have subfolders and csv files as specified in the file documentation.
- gesture_box_plot.ipynb
    - Overview: This script outputs csv files that contains data points to create box plots.
    - The first three cells are utilized to compute the length of each trial, which will be a data point. 
    - The first cell takes in the CleanedData directory and converts it into a dictionary for easier iteration based on gesture rather than subject number. The second cell contains helper methods to find the length of a trial. The third cell puts it all together and finds the length of each individual trial and adds it to a csv data file as a data point for the box plot.
    - You will need to edit the gestures_lengths_path variable in the last code cell and cleaned_data_folder path in the first cell.

