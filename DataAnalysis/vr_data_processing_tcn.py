# In[1]:
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import BSpline, make_interp_spline
import pickle
from datetime import datetime, timezone
import sys
import json


# In[4]: Dataframe Initializations

def create_columns_in_hook_removed_df(df):
    """
    Initializes an empty dataframe with columns for subject, session, trial ids as well as controller/head translation and rotations.

    Parameters
    -----
    df : dataframe
        dataframe to add new columns to
    """
    df['HeadPosX'], df['HeadPosY'], df['HeadPosZ'] = np.nan, np.nan, np.nan
    df['HeadRotX'], df['HeadRotY'], df['HeadRotZ'], df['HeadRotW'] = np.nan, np.nan, np.nan, np.nan
    df['L-HandPosX'], df['L-HandPosY'], df['L-HandPosZ'] = np.nan, np.nan, np.nan
    df['L-HandRotX'], df['L-HandRotY'], df['L-HandRotZ'], df['L-HandRotW'] = np.nan, np.nan, np.nan, np.nan
    df['R-HandPosX'], df['R-HandPosY'], df['R-HandPosZ'] = np.nan, np.nan, np.nan
    df['R-HandRotX'], df['R-HandRotY'], df['R-HandRotZ'], df['R-HandRotW'] = np.nan, np.nan, np.nan, np.nan

def create_columns_in_hook_removed_egocentralized_df(df):
    """
    Initializes an empty dataframe with columns for subject, session, trial ids as well as controller/head translation and rotations.

    Parameters
    -----
    df : dataframe
        dataframe to add new columns to
    """
    df['HeadPosX'], df['HeadPosY'], df['HeadPosZ'] = np.nan, np.nan, np.nan
    df['HeadRotX'], df['HeadRotY'], df['HeadRotZ'], df['HeadRotW'] = np.nan, np.nan, np.nan, np.nan
    df['L-HandPosU'], df['L-HandPosV'], df['L-HandPosW'] = np.nan, np.nan, np.nan
    df['L-HandDirectionU'], df['L-HandDirectionV'], df['L-HandDirectionW']= np.nan, np.nan, np.nan
    df['R-HandPosU'], df['R-HandPosV'], df['R-HandPosW'] = np.nan, np.nan, np.nan
    df['R-HandDirectionU'], df['R-HandDirectionV'], df['R-HandDirectionW'] = np.nan, np.nan, np.nan

def rename_columns(df):
    # Rename columns for trial id, head, controller positions
    df = df.rename(columns={"head_translation_x": "HeadPosX", "head_translation_y": "HeadPosY", "head_translation_z": "HeadPosZ",
                            "head_rotation_x": "HeadRotX", "head_rotation_y": "HeadRotY", "head_rotation_z": "HeadRotZ", "head_rotation_w": "HeadRotW",
                            "l_controller_translation_x": "L-HandPosX", "l_controller_translation_y": "L-HandPosY", "l_controller_translation_z": "L-HandPosZ",
                            "l_controller_rotation_x": "L-HandRotX", "l_controller_rotation_y": "L-HandRotY", "l_controller_rotation_z": "L-HandRotZ", "l_controller_rotation_w": "L-HandRotW",
                            "r_controller_translation_x": "R-HandPosX", "r_controller_translation_y": "R-HandPosY", "r_controller_translation_z": "R-HandPosZ",
                            "r_controller_rotation_x": "R-HandRotX", "r_controller_rotation_y": "R-HandRotY", "r_controller_rotation_z": "R-HandRotZ", "r_controller_rotation_w": "R-HandRotW"})
    return df



# In[5]: Hook Removal Functions

def compute_curvature(stroke_points):
    curvatures = np.zeros(len(stroke_points))  # Initialize curvature array

    for i in range(1, len(stroke_points) - 1):
        # Compute vectors
        v1 = stroke_points[i] - stroke_points[i - 1]
        v2 = stroke_points[i + 1] - stroke_points[i]
        
        if not np.all(v1 == 0) and not np.all(v2 == 0):
            # Compute curvature as the norm of the cross product, normalized by vector magnitudes
            cross_product = np.cross(v1, v2)
            curvature = np.linalg.norm(cross_product) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            # Checks if cross_product is vector 0s and updates curvature from np.nan to 0
            if np.allclose(cross_product, np.zeros(3)):
                curvature = 0

            # Add curvature for those three points to the list
            curvatures[i] = curvature
        else:
            curvatures[i] = curvatures[i-1]

    # Last point has the same curvature as the point before it
    curvatures[len(stroke_points)-1] = curvatures[len(stroke_points)-2]

    return curvatures

def remove_hooks(df):
    # Iterate through the first ten points in reverse and gets new start index based on sharp curvature
    start, end = 0, len(df)-1
    threshold = 2

    l_x = pd.to_numeric(df['L-HandPosX'], errors='coerce')
    l_y = pd.to_numeric(df['L-HandPosX'], errors='coerce')
    l_z = pd.to_numeric(df['L-HandPosX'], errors='coerce')

    l_stroke = np.array(list(zip(l_x,l_y,l_z)))
    l_curvatures = compute_curvature(l_stroke)

    l_median = np.median(l_curvatures)
    l_mad = np.median([abs(x - l_median) for x in l_curvatures])

    l_modified_z_scores = [0.6745 * (x - l_median) / l_mad if l_mad != 0 else 0 for x in l_curvatures]

    for i in range(int(len(l_curvatures)*2/5),-1,-1):
        if abs(l_modified_z_scores[i]) > threshold:
            start = i
            break

    # Iterate through the first last points and gets new end index based on sharp curvature
    for i in range(len(l_curvatures)-(int(len(l_curvatures)*2/5)), len(l_curvatures)):
        if abs(l_modified_z_scores[i]) > threshold:
            end = i-1
            break


    r_x = pd.to_numeric(df['R-HandPosX'], errors='coerce')
    r_y = pd.to_numeric(df['R-HandPosY'], errors='coerce')
    r_z = pd.to_numeric(df['R-HandPosZ'], errors='coerce')

    r_stroke = np.array(list(zip(r_x,r_y,r_z)))
    r_curvatures = compute_curvature(r_stroke)

    r_median = np.median(r_curvatures)
    r_mad = np.median([abs(x - r_median) for x in r_curvatures])

    r_modified_z_scores = [0.6745 * (x - r_median) / r_mad if r_mad != 0 else 0 for x in r_curvatures]

    for i in range(int(len(r_curvatures)*2/5),-1,-1):
        if (abs(r_modified_z_scores[i]) > threshold) and (i>start):
            start = i
            break
    for i in range(len(r_curvatures)-(int(len(r_curvatures)*2/5)), len(r_curvatures)):
        if (abs(r_modified_z_scores[i]) > threshold) and (i<end):
            end = i-1
            break

    return df.iloc[start:end]





# Egocentric Functions
# In[6]: Egocentric Functions

selected_columns = ['R-HandPosX', 'R-HandPosY', 'R-HandPosZ',
                    'R-HandRotX', 'R-HandRotY', 'R-HandRotZ', 'R-HandRotW',
                    'L-HandPosX', 'L-HandPosY', 'L-HandPosZ',
                    'L-HandRotX', 'L-HandRotY', 'L-HandRotZ', 'L-HandRotW',                    
                    'HeadPosX', 'HeadPosY', 'HeadPosZ',
                    'HeadRotX', 'HeadRotY', 'HeadRotZ', 'HeadRotW',]

## 3.1 L-handed -> R-handed (only invert translation_z for head + L/R hands)
def left_to_right_handed(data_sample, selected_columns):
    r_handed_data_sample = [] # r-handed data of the chosen sample; 21 lists
    for idx, col in enumerate(selected_columns):
        if 'PosZ' in col:
            inv_lst = [-float(val) for val in data_sample[idx]]
            
            r_handed_data_sample.append(inv_lst)
        else: # other columns not needing inverted
            r_handed_data_sample.append(data_sample[idx])
    return r_handed_data_sample

## 3.2 Data processing: Rotation 4-Quaternion to 3-direction for head + L/R hands
directional_data_names = ['R-HandPosX', 'R-HandPosY', 'R-HandPosZ', 'R-HandDirectionX', 'R-HandDirectionY', 'R-HandDirectionZ',
                         'L-HandPosX', 'L-HandPosY', 'L-HandPosZ', 'L-HandDirectionX', 'L-HandDirectionY', 'L-HandDirectionZ',
                         'HeadPosX', 'HeadPosY', 'HeadPosZ', 'HeadDirectionX', 'HeadDirectionY', 'HeadDirectionZ']

# function: Convert a quaternion into a 3D rotation matrix
def quaternion_rotation_matrix(Q):
    # Extract values from Q
    qx = float(Q[0])
    qy = float(Q[1])
    qz = float(Q[2])
    qw = float(Q[3])

    # First row of the rotation matrix
    r00 = 1.0 - 2.0 * (qy * qy + qz * qz)
    r01 = 2.0 * (qx * qy - qw * qz)
    r02 = 2.0 * (qx * qz + qw * qy)

    # Second row of the rotation matrix
    r10 = 2.0 * (qx * qy + qw * qz)
    r11 = 1.0 - 2.0 * (qx * qx + qz * qz)
    r12 = 2.0 * (qy * qz - qw * qx)

    # Third row of the rotation matrix
    r20 = 2.0 * (qx * qz - qw * qy)
    r21 = 2.0 * (qy * qz + qw * qx)
    r22 = 1.0 - 2.0 * (qx * qx + qy * qy)

    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02],
                           [r10, r11, r12],
                           [r20, r21, r22]])
    return rot_matrix

# function: Convert rotation data represented as quaterinons into a directions (3D vector)
#            by rotating a forward vector (0, 0, 1) using the given quaternion
def convertQuaternions2Directions(rotation_x_list, rotation_y_list,rotation_z_list,rotation_w_list):
    direction_x_list = []
    direction_y_list = []
    direction_z_list = []
    forward_vec = np.array([0, 0, 1])
    for i in range(len(rotation_x_list)):
        quaternion = [rotation_x_list[i],rotation_y_list[i],rotation_z_list[i],rotation_w_list[i]]
        rot_matrix = quaternion_rotation_matrix(quaternion)
        dir_vec = rot_matrix.dot(forward_vec)
        direction_x_list.append(dir_vec[0])
        direction_y_list.append(dir_vec[1])
        direction_z_list.append(dir_vec[2])
    return direction_x_list, direction_y_list, direction_z_list

# Apply to rotations of head and L/R
def quaternion_to_direction(r_handed_data_sample, selected_columns):
    directional_data_sample = []
    items = [[[0, 2], [3, 6]], [[7, 9], [10, 13]], [[14, 16], [17, 20]]] # index range for R/L/Head:[R:[trans,rot],L:[trans,rot],Head:[trans,rot]]
    # traverse R -> L -> Head in order
    for item in items: 
        # translation data
        for idx in range(item[0][0], item[0][1] + 1):
            directional_data_sample.append(r_handed_data_sample[idx])
        # rotation data
        quaternion_lists = []
        direction_x_list = []
        direction_y_list = []
        direction_z_list = []
        for idx in range(item[1][0], item[1][1] + 1):
            quaternion_lists.append(r_handed_data_sample[idx])
        if (len(quaternion_lists) == 4):
            direction_x_list, direction_y_list, direction_z_list = convertQuaternions2Directions(
                quaternion_lists[0], quaternion_lists[1], quaternion_lists[2], quaternion_lists[3])
            directional_data_sample.append(direction_x_list)
            directional_data_sample.append(direction_y_list)
            directional_data_sample.append(direction_z_list)
    return directional_data_sample

## 3.3 World -> Egocentric coordinates (head + L/R hands -> L/R hands) 
#   and reformat the sample as [[...],[...],...[...]], a list of 12 signals (lists)
egocentric_data_names = ['R-HandPosU', 'R-HandPosV', 'R-HandPosW', 'R-HandDirectionU', 'R-HandDirectionV', 'R-HandDirectionW',
                         'L-HandPosU', 'L-HandPosV', 'L-HandPosW', 'L-HandDirectionU', 'L-HandDirectionV', 'L-HandDirectionW']

# function construct a head space coordinate system consisting of three basis vectors, u, v, w for EACH trial
def buildHeadSpaceCoordVectors(head_direction_x_list, head_direction_y_list, head_direction_z_list):
    # average head direction vectors across all frames in the trial
    avg_head_direction_x = sum(head_direction_x_list)/len(head_direction_x_list)
    avg_head_direction_y = sum(head_direction_y_list)/len(head_direction_y_list)
    avg_head_direction_z = sum(head_direction_z_list)/len(head_direction_z_list)
    
    # calculate head space coordinate vectors, u, v, w
    head_space_w = 1.0 * np.array([avg_head_direction_x, avg_head_direction_y, avg_head_direction_z]) # w is opposite of the head direction
    head_space_v = np.array([0, 1, 0])
    head_space_u = np.cross(head_space_v, head_space_w)
    head_space_v = np.cross(head_space_w, head_space_u)

    return head_space_u, head_space_v, head_space_w

# function: convert hand data from world to head
def convert_hand_world_to_head(avg_head_translation, rot_matrix, hand_translation_x_list,  hand_translation_y_list,  hand_translation_z_list,
                                hand_direction_x_list,  hand_direction_y_list,  hand_direction_z_list):
    hand_translation_u_list = []
    hand_translation_v_list = []
    hand_translation_w_list = []
    hand_direction_u_list = []
    hand_direction_v_list = []
    hand_direction_w_list = []

    # convert hand data world -> space, frame by frame
    for idx in range(len(hand_translation_x_list)):
        # Translation data: (Already correct)
        hand_translation_u = float(hand_translation_x_list[idx]) - float(avg_head_translation[0])
        hand_translation_v = float(hand_translation_y_list[idx]) - float(avg_head_translation[1])
        hand_translation_w = float(hand_translation_z_list[idx]) - float(avg_head_translation[2])
        hand_translation = rot_matrix.dot(np.array([hand_translation_u, hand_translation_v, hand_translation_w]))
        hand_translation_u_list.append(hand_translation[0])
        hand_translation_v_list.append(hand_translation[1])
        hand_translation_w_list.append(hand_translation[2])

        # Direction data: (Change this to point toward the origin)
        # Compute the direction from the hand position to the origin
        direction_to_head = 1.0 * np.array([hand_translation_u, hand_translation_v, hand_translation_w])  # Direction to the origin
        hand_direction_u_list.append(direction_to_head[0])
        hand_direction_v_list.append(direction_to_head[1])
        hand_direction_w_list.append(direction_to_head[2])

    return hand_translation_u_list, hand_translation_v_list, hand_translation_w_list, hand_direction_u_list, hand_direction_v_list, hand_direction_w_list

def world_to_headspace(directional_data_sample, directional_data_names):
    egocentric_data_sample = []
    # obtain head translation data in world space
    # converts to float bc for some reason, some of the data is are strings
    head_translation_x_list = [float(i) for i in directional_data_sample[12]]
    head_translation_y_list = [float(i) for i in directional_data_sample[13]]
    head_translation_z_list = [float(i) for i in directional_data_sample[14]]

    # average head translation data -> averaged head position in world
    avg_head_translation = []
    avg_head_translation.append(sum(head_translation_x_list)/len(head_translation_x_list))
    avg_head_translation.append(sum(head_translation_y_list)/len(head_translation_y_list))
    avg_head_translation.append(sum(head_translation_z_list)/len(head_translation_z_list))

    # obtain head direction data in world space
    head_direction_x_list = directional_data_sample[15]
    head_direction_y_list = directional_data_sample[16]
    head_direction_z_list = directional_data_sample[17]
    
    # build coordiante vectors of the head space: u, v, w
    head_space_u, head_space_v, head_space_w = buildHeadSpaceCoordVectors(head_direction_x_list=head_direction_x_list, 
                                                                          head_direction_y_list=head_direction_y_list,
                                                                          head_direction_z_list=head_direction_z_list)

    # construct rotation matrix transforming vectors from world to head space
    rot_matrix = np.array([head_space_u.tolist(), # u
                           head_space_v.tolist(), # v
                           head_space_w.tolist()]) # w
    
    # convert RIGHT hand data from world to head space
    r_translation_u_list, r_translation_v_list, r_translation_w_list, \
       r_direction_u_list,r_direction_v_list, r_direction_w_list \
            = convert_hand_world_to_head(avg_head_translation, rot_matrix, directional_data_sample[0], directional_data_sample[1],directional_data_sample[2],\
                                         directional_data_sample[3], directional_data_sample[4],directional_data_sample[5])

    # convert LEFT hand data from world to head space
    l_translation_u_list, l_translation_v_list, l_translation_w_list, \
        l_direction_u_list, l_direction_v_list, l_direction_w_list \
            = convert_hand_world_to_head(avg_head_translation, rot_matrix, directional_data_sample[6], directional_data_sample[7],directional_data_sample[8],\
                                         directional_data_sample[9], directional_data_sample[10],directional_data_sample[11])
    
    # add the converted data
    egocentric_data_sample.append(r_translation_u_list) # right hand
    egocentric_data_sample.append(r_translation_v_list)
    egocentric_data_sample.append(r_translation_w_list)
    egocentric_data_sample.append(r_direction_u_list)
    egocentric_data_sample.append(r_direction_v_list)
    egocentric_data_sample.append(r_direction_w_list)
    egocentric_data_sample.append(l_translation_u_list) # left hand
    egocentric_data_sample.append(l_translation_v_list)
    egocentric_data_sample.append(l_translation_w_list)
    egocentric_data_sample.append(l_direction_u_list)
    egocentric_data_sample.append(l_direction_v_list)
    egocentric_data_sample.append(l_direction_w_list)

    return egocentric_data_sample

def smooth_and_resample(df, n_points=128, k=3):
    new_df = pd.DateFrame()

    """Smooths stroke using B-spline and resamples points evenly along the curve."""
    for col in df.columns:
        vals = np.array(df[col])
        t = np.linspace(0, 1, len(vals))

        # Fit B-splines to smooth the data
        spl = make_interp_spline(t, vals, k=k)

        # Generate new t values for resampling
        t_new = np.linspace(0, 1, n_points)

        vals_resampled = spl(t_new)

        new_df[col] = vals_resampled

    return new_df

    '''
    positions = np.array(positions)
    directions = np.array(directions)

    t = np.linspace(0, 1, len(positions[0]))

    # Fit B-splines to smooth the position data
    spl_x = make_interp_spline(t, positions[0, :], k=k)
    spl_y = make_interp_spline(t, positions[1, :], k=k)
    spl_z = make_interp_spline(t, positions[2, :], k=k)

    # Fit B-splines to the direction vectors directly 
    spl_dx = make_interp_spline(t, directions[0, :], k=k)
    spl_dy = make_interp_spline(t, directions[1, :], k=k)
    spl_dz = make_interp_spline(t, directions[2, :], k=k)
    
    # Generate new t values for resampling
    t_new = np.linspace(0, 1, n_points)

    # Resampled positions
    x_resampled = spl_x(t_new)
    y_resampled = spl_y(t_new)
    z_resampled = spl_z(t_new)
    
    # Resampled directions (tangent vectors)
    dx_resampled = spl_dx(t_new)
    dy_resampled = spl_dy(t_new)
    dz_resampled = spl_dz(t_new)

    # Pack results
    resampled_positions = (x_resampled, y_resampled, z_resampled)
    resampled_directions = (dx_resampled, dy_resampled, dz_resampled)

    return resampled_positions, resampled_directions
    '''



def normalize(stroke, min_stroke, max_stroke):
    # Based off of the min max across all strokes for each signal (L_X, L_Y, R_Z, etc)
    min_x, min_y, min_z = min_stroke
    max_x, max_y, max_z = max_stroke

    # Calculate the range for each axis
    range_x = max_x - min_x
    range_y = max_y - min_y
    range_z = max_z - min_z

    # Determine the largest range to use as the scaling factor
    max_range = max(range_x, range_y, range_z)

    # Normalize stroke
    norm_x1 = [((x - min_x) / max_range) for x in stroke[0]]
    norm_y1 = [((y - min_y) / max_range) for y in stroke[1]]
    norm_z1 = [((z - min_z) / max_range) for z in stroke[2]]

    return (norm_x1, norm_y1, norm_z1)




# In[8]: Data Processing -> Converting to Summary Statistics
def process_data(input_df):
    input_df = rename_columns(input_df)

    # Remove Hooks
    hook_removed_df = pd.DataFrame()
    create_columns_in_hook_removed_df(hook_removed_df)
    hook_removed_df = pd.concat([hook_removed_df, remove_hooks(input_df)])

    # Egocentralizing the data
    egocentric_df = pd.DataFrame()
    create_columns_in_hook_removed_egocentralized_df(egocentric_df)

    data_sample = [] # original data of the chosen sample; 21 lists
    for col in selected_columns:
        data_sample.append(hook_removed_df[col].tolist())
        
    # 3.2
    directional_data_sample = quaternion_to_direction(r_handed_data_sample=data_sample, selected_columns=selected_columns)
    # 3.3
    egocentric_data_sample = world_to_headspace(directional_data_sample=directional_data_sample, directional_data_names=directional_data_names)
    
    # For reference
    #left_points = (list(zip(egocentric_data_sample[6], egocentric_data_sample[7], egocentric_data_sample[8])))
    #right_points = (list(zip(egocentric_data_sample[0], egocentric_data_sample[1], egocentric_data_sample[2])))
    
    # Filtering the group to rename columns from rotation to direction for egocentric output since there are excessive columns in rotation
    hook_removed_df = hook_removed_df.loc[:,["HeadPosX", "HeadPosY", "HeadPosZ", "HeadRotX", "HeadRotY", "HeadRotZ", "HeadRotW", "L-HandPosX", "L-HandPosY", "L-HandPosZ", "L-HandRotX", "L-HandRotY", "L-HandRotZ", "R-HandPosX", "R-HandPosY", "R-HandPosZ", "R-HandRotX", "R-HandRotY", "R-HandRotZ"]]

    hook_removed_df = hook_removed_df.rename(columns={
                        "L-HandPosX": "L-HandPosU", "L-HandPosY": "L-HandPosV", "L-HandPosZ": "L-HandPosW",
                        "L-HandRotX": "L-HandDirectionU", "L-HandRotY": "L-HandDirectionV", "L-HandRotZ": "L-HandDirectionW",
                        "R-HandPosX": "R-HandPosU", "R-HandPosY": "R-HandPosV", "R-HandPosZ": "R-HandPosW",
                        "R-HandRotX": "R-HandDirectionU", "R-HandRotY": "R-HandDirectionV", "R-HandRotZ": "R-HandDirectionW"})
    
    # Update values for egocentric position & directions
    hook_removed_df['L-HandPosU'], hook_removed_df['L-HandPosV'], hook_removed_df['L-HandPosW'] = egocentric_data_sample[6], egocentric_data_sample[7], egocentric_data_sample[8]
    hook_removed_df['L-HandDirectionU'], hook_removed_df['L-HandDirectionV'], hook_removed_df['L-HandDirectionW'] = egocentric_data_sample[9], egocentric_data_sample[10], egocentric_data_sample[11]
    hook_removed_df['R-HandPosU'], hook_removed_df['R-HandPosV'], hook_removed_df['R-HandPosW'] = egocentric_data_sample[0], egocentric_data_sample[1], egocentric_data_sample[2]
    hook_removed_df['R-HandDirectionU'], hook_removed_df['R-HandDirectionV'], hook_removed_df['R-HandDirectionW'] = egocentric_data_sample[3], egocentric_data_sample[4], egocentric_data_sample[5]

    egocentric_df = pd.concat([egocentric_df, hook_removed_df])


    resampled_df = smooth_and_resample(egocentric_df)
    preprocessed_df = normalize(resampled_df)

    return preprocessed_df





# RUN HERE
# In[12]: Model Prediction Functions
label_encoder = {0: 'Pan Down',
                 1: 'Pan Left',
                 2: 'Pan Right',
                 3: 'Pan Up',
                 4: 'Rot Back X',
                 5: 'Rot Clock Y',
                 6: 'Rot Counter Y',
                 7: 'Rot Forward X',
                 8: 'Rot Left Z',
                 9: 'Rot Right Z',
                 10: 'Zoom In',
                 11: 'Zoom Out'
                 }

def predict_gesture(input_df, model):
    processed_df = process_data(input_df)
    # Fix the function above
    processed_df = processed_df[model.feature_names_in_]      # Reorganizing column

    y_pred = model.predict(processed_df)
    y_pred = numeric_to_text_label(y_pred)

    return y_pred

def numeric_to_text_label(label_num_list):
    label_text_list = []

    for label_num in label_num_list:
        label_text_list.append(label_encoder[label_num])

    return label_text_list[0]
    
def run(input_dict):
    model_path = os.path.join('C:\\Workspace\\VRmotion-3dmodeling\\open-brush\\Assets\\StreamingAssets\\Models\\tcn_model.pkl')
    input_df = pd.DataFrame(input_dict)

    with open(model_path, "rb") as file:
        loaded_model = pickle.load(file)
        prediction = predict_gesture(input_df, loaded_model)

        return prediction



import sys
import json

def predict_from_json(json_string):
    data = json.loads(json_string)

    result = run(data)
    return json.dumps(result)