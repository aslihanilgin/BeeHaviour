# Running the program

## Activating the Conda environment
This project has a few pre-requisities that need to be installed. The following table shows the packages you need to install inside your Conda environment.

Package Name | matplotlib | numpy | pandas | python | roboflow | opencv-python
--- | --- | --- | --- |--- |--- |--- |--- |---
Version | 3.7.0 | 1.24.2 | 1.5.2 | 3.11.0 | 0.2.32 | 4.7.0.68
Activate the Conda environment using:

`conda activate bee-behaviour`

## Extracting frames
Run the program from the root folder using:

*python <dir_to_frame_extraction.py_file> <dir_to_video>*

`python frame-extraction/frame_extraction.py frame-extraction/videos/test-video-short.MOV`

## Extracting information from frames
Run the program from the root folder using:

*python <dir_to_info_extraction.py_file>*

`python info-extraction/info_extraction.py`

## Manipulate information in the CSV
To manipulate information in the information CSV file and to use the information to compute further calculations, run the manipulation file using:

*python <dir_to_table_manipulation.py_file> <frame_rate_of_your_video>*

`python info-extraction/table_manipulation.py 25`