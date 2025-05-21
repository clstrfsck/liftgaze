# Gaze tracking
This project contains a sample project for training and applying gaze
information to input video files and raw, synchronised gaze data.

## Setup
### Install the dependencies:
```
$ pip3 install -r requirements.txt
```

### Assemble input files
In the `./input` directory place:
- `lift.mp4` the input image file
- `lift.tsv` the tab-separated file with synchronised gaze information
- `lift.yaml` the project information file— see below for details

Example `lift.yaml`:
```
path: .
train: train
val: val

# Classes
names:
  0: weight
  1: bar
  2: person
```

## Step 1
Split the video file into frames.
- Copy the input video to `./input/lift.mp4` (you may need to create this directory)
- Run the `00split.py` file

This will extract all the frames in the video into the `./output` directory as `.jpg` files.  Each filename will include the frame number and video timestamp and named `frame_{frameNumber}_{timestampMicroseconds}.jpg`.

## Step 2
Sample some images from the video frames for training.  About 80% of the samples should be used for training, and 20% of the frames for validation.

Each of these images will need to be annotated with the features to be identified.

I used 10 total frames, 8 for training and 2 for validation.  This seemed to work pretty well for the sample data used.

- Run the `01sample.py` file.  This will copy a random set of 12 files to the `./train` directory.
- Inspect the resultant images.
  - There is no point including images which will have no annotations in them.  If you have some of these, remove them.
  - If you end up with too few images after removing them, empty the directory and restart the step.

## Step 2a
Annotate the images in the sample directory.  I used https://www.makesense.ai/ for this, but anything should work, as long as it outputs data in YOLO format.

I used 8 training images and 2 validation images with annotations for each.

I used labels for:
- weight
- bar
- person

Order needs to match the information in `lift.yaml` in the setup section.

The result data should be downloaded in YOLO format and the individual `.txt` files placed in the `./train` directory with the training images.

Move approximately 20% of the images and their annotation files into a `./val` directory, creating it if it does not exist.

## Step 3
Train YOLO on our training data.

- Run `./02train.py`.  This will produce a trained model in `runs/train/yolo11-lift/weights/best.pt`.

Check the confusion matrix in `./runs/train/yolo11-lift/confusion_matrix_normalized.png` to make sure that each label is well identified.
Also check the predictions in `runs/train/yolo11-lift2` to make sure the features are correctly identified and labelled.

This is by far the most time consuming process here, but should only need to be run once for each similar set of input videos.

## Step 4
Using the model generated in step 3, run the predictions on our data.

- Run `./03predict.py`.  This will output `.jpg` and `.json` image and hitbox information in JSON format into the `./runs/detect/predict/` directory for each frame in the `./output` directory that was created in step 1.

It might be worthwhile reviewing the resultant images before proceeding to the next stage.

## Step 5
Using the output images from step 4, together with the gaze data, output a video with labelled features and gaze location.

- Run `./04video.py`.  This will output a `lift_predict.mp4` video.
