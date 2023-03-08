# Author: A. Ilgin Okan

from roboflow import Roboflow
import csv
from os import listdir, getcwd
import config

# https://stackoverflow.com/questions/62775713/background-substractor-python-opencv-remove-granulation

# connect to the Roboflow API
rf = Roboflow(api_key=config.roboflow_api_key)
project = rf.workspace().project("behaviours")
model = project.version(1).model

# create video frame info dicts
video_frames = {}
frames = []

# get frame names
for frame_name in sorted(listdir("frame-extraction/videos/test-video-short-frames")):
    frames.append(frame_name)

# predict and get bee info from frames
for frame in frames:
    # infer on a local image
    frame_dir = getcwd() + "/frame-extraction/videos/test-video-short-frames/" + frame
    prediction = model.predict(frame_dir, confidence=40, overlap=30).json()


    # create a key for the frame in the dict
    if frame not in video_frames:
        video_frames[frame] = {}

    if prediction['predictions'] != []:
        # TODO: only getting the left and bottom corner coords
        video_frames[frame] = {'x_coord' : prediction['predictions'][0]['x']}
        video_frames[frame].update({'y_coord' : prediction['predictions'][0]['y']})

    else:
        video_frames[frame] = {'x_coord' : None}
        video_frames[frame].update({'y_coord' : None})

    # https://www.scaler.com/topics/how-to-create-a-csv-file-in-python/
    with open('info-extraction/bumbleebee_test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["Video", "Frame", "X_coord", "Y_coord"])
        # collect data for each video frame into csv file
        for frame in video_frames:
            writer.writerow(["Sample_video", frame, video_frames[frame]['x_coord'], video_frames[frame]['y_coord']])

    # visualize your prediction
    # save_dir = getcwd() + "/frame-extraction/videos/predicted-frames/"
    # model.predict(frame_dir, confidence=40, overlap=30).save(save_dir + "prediction_"+ frame +".jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())