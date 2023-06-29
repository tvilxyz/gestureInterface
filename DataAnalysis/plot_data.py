# import necessary packages
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from plotnine import *
import statsmodels.api as sm

from sklearn.linear_model import LinearRegression # Linear Regression Model
from sklearn.preprocessing import StandardScaler #Z-score variables

from sklearn.model_selection import train_test_split # simple TT split cv

# importing data
sub_1_1_pan_right_DF = pd.read_csv("../Data/Sub1/Instructional/session_I_PanRight_subjID_1_04-14-23_02-30-22.csv")

sub_1_1_pan_right_DF.drop(sub_1_1_pan_right_DF[(sub_1_1_pan_right_DF['trigger_pull_amount_left'] == 0) & (sub_1_1_pan_right_DF['trigger_pull_amount_right'] == 0)].index, inplace=True)

counter = ["time", "absolute_time", "left_handed", "right_handed", "trigger_pull_amount_left", "trigger_pull_amount_right", "gesture_counter_UI", "x_pressed", "x_counter", "gesture_counter"]
sub_1_1_pan_right_DF_counter = sub_1_1_pan_right_DF[counter]

translation = ["r_controller_translation_x", "r_controller_translation_y", "r_controller_translation_z", "l_controller_translation_x", "l_controller_translation_y", "l_controller_translation_z"]
sub_1_1_pan_right_DF_translation = sub_1_1_pan_right_DF[translation]

zscore = StandardScaler()
sub_z_1_1_pan_right_DF = pd.DataFrame(zscore.fit_transform(sub_1_1_pan_right_DF_translation))

sub_z_1_1_pan_right_DF.columns = ['r_controller_translation_x', 'r_controller_translation_y', 'r_controller_translation_z', 'l_controller_translation_x', 'l_controller_translation_y', 'l_controller_translation_z']

sub_1_1_pan_right_DF_counter.insert(0, 'index', range(0, 0 + len(sub_1_1_pan_right_DF)))

sub_z_1_1_pan_right_DF.insert(0, 'index', range(0, 0 + len(sub_z_1_1_pan_right_DF)))

merged_sub_z_1_1_pan_right_DF = pd.merge(left=sub_1_1_pan_right_DF_counter, right=sub_z_1_1_pan_right_DF, left_on='index', right_on='index')
