# How to Use

## Install requirements

This command will install the needed dependencies.

```
pip3 install -r requirements.txt
```

## Create a QR Code for a Voter

Run the following command:

```
python3 main.py register --id <input> --name <input>
```

Provide the Jamaat ID number and name of the voter.
A QR code will appear as a PDF. You can now print it.

for more information and additional help run:

```
python3 main.py register --help
```

## Start the Voting Process

Run the following command to launch the voting functionality. It will use per default the laptop camera, as input source.

```
python3 main.py vote
```

Now, hold the printed QR code in front of the camera.
When it is detected, the name and ID number will be shown on the video stream.
To terminate the windows press `q`.

To use multiple cameras or video files as input sources and configure different detection methods, run this command to learn more:

```
python3 main.py vote --help
```

# Development

## Interchangeable QR-Code Detection

To extend QRvote with additional QR code detection libraries and algorithms, define a custom class that inherits from the `DetectionStrategy` class and implements its abstract method `detect_votes_from_frame(frame)` using your own QR code detection logic. Make sure to register the newly created class in the `detection_strategies` list within `config_detection_strategies.py`. Once registered, it will be available and selectable in the menu.

# Remarks

- The system can detect multiple QR codes at the same time.
- Detection is not optimized for long distances yet.
