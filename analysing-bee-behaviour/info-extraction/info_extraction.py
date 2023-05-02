# Author: A. Ilgin Okan

from roboflow import Roboflow
import csv
import sys
import re
from os import listdir, getcwd, walk
import config
from pred_val_extraction import *

# https://stackoverflow.com/questions/62775713/background-substractor-python-opencv-remove-granulation

# connect to the Roboflow API
rf = Roboflow(api_key=config.roboflow_api_key)
project = rf.workspace().project("behaviours")
model = project.version(1).model

video_frames_dict = {}
frames = []

video_name = sys.argv[1]

extracted_frames_dir = getcwd() +"/frame-extraction/videos/"+video_name+"-frames"

# https://stackoverflow.com/questions/55946720/sort-a-list-by-specific-location-in-string
def sort_frames(item):
    #You need to return the key you want to sort on
    return int(item.split('-')[0])

for frame_name in sorted(listdir(extracted_frames_dir), key=sort_frames):
    frames.append(frame_name)


# https://www.scaler.com/topics/how-to-create-a-csv-file-in-python/
with open('info-extraction/bumblebee_test.csv', 'w', newline='') as file:
# TODO: for the whole loop 
    writer = csv.writer(file)
    
    column_names = ["video", "frame_no", "frame_name", "video_time", "x_mid", "y_mid", "velocity", "walk"
                    "updown", "fly", "pause", "groom", "drop", "fan", "other"]
    writer.writerow(column_names)

    # predict and get bee info from frames
    for frame in frames:
        # infer on a local image
        frame_dir = getcwd() + "/frame-extraction/videos/test-video-short-frames/" + frame
        prediction = model.predict(frame_dir, confidence=40, overlap=30).json()

        # create a key for the frame in the dict
        if frame not in video_frames_dict:
            video_frames_dict[frame] = {}

        if prediction['predictions'] != []:
            pred_val = pred_val_extraction(prediction)
            video_frames_dict[frame].update({'x_mid' : pred_val.x_mid})
            video_frames_dict[frame].update({'y_mid' : pred_val.y_mid})

        else:
            video_frames_dict[frame] = {'x_mid' : None}
            video_frames_dict[frame].update({'y_mid' : None})

        # get timestamp of frame
        time_digits = re.findall(r'\d+', frame)
        mins, secs, milisecs = time_digits[2], time_digits[3], time_digits[4]
        video_time = mins + ":" + secs + ":" + milisecs

        # get frame number
        frame_no = time_digits[0]

        # write to csv file
        frame_values = ["Sample_video", frame_no, frame, video_time, video_frames_dict[frame]['x_mid'], video_frames_dict[frame]['y_mid']]
        writer.writerow(frame_values)