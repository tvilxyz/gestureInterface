import math
import pandas as pd

def read_file(filePath):
    file = pd.read_csv(filePath)
    return file


def get_dlength(pt1X, pt1Y, pt1Z, pt2X, pt2Y, pt2Z):
    xDistance = pt2X - pt1X
    yDistance = pt2Y - pt1Y
    zDistance = pt2Z - pt1Z
    length = math.sqrt((xDistance)**2 + (yDistance)**2 + (zDistance)**2)
    return length

def get_sum_dlength(df, trialNum):
    df.drop(df[(df["trigger_pull_amount_left"] == 0) & (df["trigger_pull_amount_right"] == 0)].index, inplace=True)
    df.drop(df[(df['gesture_counter_UI']) != trialNum].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df)

path = "C:\\Users\\vrelax\\Desktop\\VRelax\\gestureInterface\\Data\\cleaned_session_I_ZoomOut_subjID_1_04-14-23_02-31-52.csv"
file = read_file(path)
get_sum_dlength(file, 1)