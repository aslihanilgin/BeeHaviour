import pandas as pd
from os import getcwd
import sys
import numpy as np
import re
from pred_val_extraction import *

def main():

    csv_dir = getcwd() + "/info-extraction/"
    info_df = pd.read_csv(csv_dir + 'bumblebee_test.csv')
    
    # https://stackoverflow.com/questions/29007830/identifying-consecutive-nans-with-pandas
    w_NaN_count_df = pd.concat([
                    info_df,
                    (
                        info_df.x_mid.isnull().astype(int)
                        .groupby(info_df.x_mid.notnull().astype(int).cumsum())
                        .cumsum().to_frame('consec_NaN_count')
                    )
                ],
                axis=1
            )

    fps_rate = int(sys.argv[1]) # change according to fps of video

    w_NaN_count_df = interpolateMissingCoordVals(w_NaN_count_df, fps_rate)

    w_NaN_count_df = computeVelocityVals(w_NaN_count_df, fps_rate)

    w_NaN_count_df = w_NaN_count_df.loc[:, w_NaN_count_df.columns!='consec_NaN_count']

    csv_save_dir = csv_dir + "after_manipulation.csv"
    
    w_NaN_count_df.to_csv(csv_save_dir, index=False)


# Extract time stamp information for analysis
def getTimeStampInfo(time):
    # get timestamp of frame
    time_digits = re.findall(r'\d+', time)
    mins, secs, milisecs = time_digits[0], time_digits[1], time_digits[2]

    return mins, secs, milisecs

def interpolateMissingCoordVals(w_NaN_count_df, fps_rate):

    for frame in w_NaN_count_df['frame_no']:
        if frame == 0:
            continue
        current_NaN_count = w_NaN_count_df['consec_NaN_count'][frame]
        prevFrame_NaN_count = w_NaN_count_df['consec_NaN_count'][frame-1]

        frame_diff = prevFrame_NaN_count - current_NaN_count

        if frame_diff != 0 and frame_diff != -1: # -1 means consec_NaN_count is increasing
            if frame_diff <= fps_rate: # no bee detected for less than a second
                # means it was false negative, need to interpolate specific section of the df
                sectioned_df = w_NaN_count_df[frame-frame_diff-1:frame+1] # TODO: frame+1 will need to be checked

                xmid_ymid_only_df = sectioned_df[['frame_no', 'x_mid', 'y_mid']]
                interpolated_df = xmid_ymid_only_df.interpolate(method ='linear', limit_direction ='both')
                interpolated_df = interpolated_df.round(1) # round the interpolation values to one decimal 
                
                # get each interpolated section and put them in frameno_xmid_ymid_consNaNcount_df 
                for frame in interpolated_df['frame_no']:
                    w_NaN_count_df.at[frame, 'x_mid'] = interpolated_df.at[frame, 'x_mid']
                    w_NaN_count_df.at[frame, 'y_mid'] = interpolated_df.at[frame, 'y_mid']

    return w_NaN_count_df

def computeVelocityVals(w_NaN_count_df, fps_rate):

    non_NaN_counter = 0

    for frame in w_NaN_count_df['frame_no']:
        
        if (frame%fps_rate == 0 and frame != 0):

            frame_minus_fps = frame - fps_rate

            try:
                
                # if all the values within that range isn't NaN
                # -> means that some values exist, but there are some NaNs as well
                if (pd.notna(w_NaN_count_df['y_mid'][frame_minus_fps:frame]).all()):
                      
                    y2_coord = w_NaN_count_df.at[frame, 'y_mid']
                    y1_coord = w_NaN_count_df.at[frame_minus_fps, 'y_mid']

                    _, secs2, _ = getTimeStampInfo(w_NaN_count_df.at[frame, 'video_time'])
                    _, secs1, _ = getTimeStampInfo(w_NaN_count_df.at[frame_minus_fps, 'video_time'])

                    t2 = int(secs2)
                    t1 = int(secs1)

                    velocity = pred_val_extraction.compute_velocity(y2_coord, y1_coord, t2, t1)

                    for frame in range(frame_minus_fps, frame):
                        w_NaN_count_df.at[frame, 'velocity'] = velocity
                
                else: # there are some na values

                    if (pd.isna(w_NaN_count_df['y_mid'][frame_minus_fps:frame]).all()): # if all is na

                        continue
                    else: # only some y_mid values are na

                        # https://stackoverflow.com/questions/47414848/pandas-select-all-columns-without-nan
                        nonNaN_vals_df = w_NaN_count_df[frame_minus_fps:frame][pd.notna(w_NaN_count_df['y_mid'][frame_minus_fps:frame])]

                        first_frame_w_non_NaN_val = nonNaN_vals_df['frame_no'].iloc[0]
                        last_frame_w_non_NaN_val = nonNaN_vals_df['frame_no'].iloc[-1]

                        y2_coord = nonNaN_vals_df[nonNaN_vals_df['frame_no']==last_frame_w_non_NaN_val]['y_mid'].item()
                        y1_coord = nonNaN_vals_df[nonNaN_vals_df['frame_no']==first_frame_w_non_NaN_val]['y_mid'].item()

                        # assigned time values to assume the time difference as 1 second for calculation
                        t2 = 2
                        t1 = 1

                        velocity = pred_val_extraction.compute_velocity(y2_coord, y1_coord, t2, t1)

                        for frame in range(first_frame_w_non_NaN_val, last_frame_w_non_NaN_val+1):                          
                            w_NaN_count_df.loc[w_NaN_count_df.frame_no == frame, 'velocity'] = velocity
                        
                
            except IndexError:
                # Index Out of Bound 
                print("INDEX ERROR")
                continue

        else:
            continue

    return w_NaN_count_df


# Start table manipulation
main()
