# How to Use

## Install requirements

```
pip3 install -r requirements.txt
```

## Create a QR Code for a Voter

Run the following command:

```
python3 main.py
```

Choose Menu Option 1.
Enter the Jamaat ID number and name of the voter.
A QR code will appear in your web browser. You can now print it.

## Start the Voting Process

Run the command again:

```
python3 main.py
```

Choose Menu Option 2.
Enter the camera or video sources.

**By default, the laptop camera is 0.**
Example:
`Enter sources separated by comma (camera IDs or file paths): 0`

You can also use a video file. Example:
`Enter sources separated by comma (camera IDs or file paths): videos/camera_stream_1`

You can use multiple sources (like several cameras or video files) by separating them with commas. Example:
`Enter sources separated by comma (camera IDs or file paths): 0,1,2,3,videos/camera_stream_1,videos/camera_stream_2`

Now, hold the printed QR code in front of the camera.
When it is detected, the name and ID number will be shown on the video stream.

## Remarks:

- The system can detect multiple QR codes at the same time.
- Detection is not optimized for long distances yet.
