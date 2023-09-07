# Gesture Interface

## Important Scripts (Ordered):
- clean_file.py
    - Overview: This script provides methods to help clean data files more efficiently and organized. Overall, it takes in a data file and removes trials that have been striked (when the x button is pressed and the x_counter increases).
    - Script prerequisites:
        - n/a
- export_clean_files.py:
    - Overview: This script cleans data files by removing trials that have been striked and exports the new csv files to a specified CleanedData folder.
    - Script prerequisites:
        - clean_file.py
- all_graph_vis.ipynb:
    - Overview: This script visualizes participants' hand motion data. It outputs two different html files. The first is an individual figure of all of the trials in a single participant session. The second groups all of the individual single participant sessions for a single gesture on one file to view all simultaneously.
    - Script prerequisites: 
        - export_clean_files.py
            - Can only use the files that have been exported by this script.
- metric_calculations.ipynb
    - Overview: Performs metric calculations for specified features of the participants' gesture data. It then outputs the measurement value calculated for each trial and exports it as csv file. For each gesture, there will be two files for freeform and instructional. It will be used to generate box plots.
    - Script prerequisites:
        - export_clean_files.py
            - Can only use the files that have been exported by this script.
- data_summary.py
    - Overview: Summarizes the metric calculations of each gesture session such as max, min, mean, etc.
    - Script prerequisites:
        - metric_calculations.ipynb
            - Can only use the files that have been exported by this script.
