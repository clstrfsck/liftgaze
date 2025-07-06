#!/usr/bin/env python3

import cv2
import pandas as pd

from bisect import bisect_left
from numpy import isfinite
from tqdm import tqdm

from files import images_in_dir
from project import PROJECT_NAME, INPUT_DIR, YOLO_PREDICT_DIR

LOOK_FILE = INPUT_DIR / f"{PROJECT_NAME}.tsv"
OUTPUT_FILE = f"{PROJECT_NAME}_predict.mp4"
TRAIL_LENGTH = 50  # Number of previous points to draw
SPAN_LENGTH = 1  # Number of frames to average for smoothing, 1 for no smoothing
DOT_SIZE = 10  # Size of the gaze point dot

print(f"Reading look points from '{LOOK_FILE}'")
lookPoints = pd.read_csv(LOOK_FILE, sep = '\t')
xPoints = list(lookPoints["Gaze point X"].ewm(span = SPAN_LENGTH).mean())
yPoints = list(lookPoints["Gaze point Y"].ewm(span = SPAN_LENGTH).mean())
timestampsUs = list(lookPoints["Recording timestamp"])
if len(xPoints) != len(yPoints) or len(xPoints) != len(timestampsUs):
    raise ValueError("Look points, timestamps, and gaze points must have the same length")

files = images_in_dir(YOLO_PREDICT_DIR)
if len(files) == 0:
    raise ValueError(f"No images found in '{YOLO_PREDICT_DIR}'")
files.sort(key=lambda x: int(x.stem.split("_")[1]))  # Sort by frame number

# Get the dimensions of the first image
first_image = cv2.imread(files[0])
image_width = first_image.shape[1]
image_height = first_image.shape[0]
fps = 25  # FIXME: Should read from original video

print(f"Writing video to '{OUTPUT_FILE}' with {len(files)} frames, {image_width}x{image_height} at {fps} FPS")
progressBar = tqdm(total=len(files), desc="Writing video frames", unit="frame")
vidwriter = cv2.VideoWriter(OUTPUT_FILE, cv2.VideoWriter_fourcc(*"mp4v"), fps, (image_width, image_height))
ps = []
for file in files:
    img = cv2.imread(file)
    timestampUs = int(file.stem.split("_")[2])
    # Linear interpolation of gaze points
    ip = bisect_left(timestampsUs, timestampUs)
    (x, y) = (None, None)
    if ip > 0:
        (t1, t2) = timestampsUs[ip - 1:ip + 1]
        (x1, x2) = xPoints[ip - 1:ip + 1]
        (y1, y2) = yPoints[ip - 1:ip + 1]
        # If we have two sets of points, linearly interpolate the gaze point
        if isfinite(x1) and isfinite(y1) and isfinite(x2) and isfinite(y2):
            x = round(x1 + (x2 - x1) * (timestampUs - t1) / (t2 - t1))
            y = round(y1 + (y2 - y1) * (timestampUs - t1) / (t2 - t1))
            if x < 0 or y < 0 or x >= image_width or y >= image_height:
                print(f"Warning: Gaze point ({x}, {y}) out of bounds for image size {image_width}x{image_height}")
    ps.append((x, y))
    prev = (None, None)
    # Draw the trail of previous points
    for (x, y) in ps[-TRAIL_LENGTH:-1]:
        (xp, yp) = prev
        if x and y and prev and xp and yp:
            cv2.line(img, prev, (x, y), (0, 255, 0), 1)
        prev = (x, y)
    (x, y) = ps[-1]
    if x and y:
        # Draw a outlined circle at the gaze point
        cv2.circle(img, (x, y), DOT_SIZE, (128, 255, 128), -1)
        cv2.circle(img, (x, y), DOT_SIZE, (0, 255, 0), 2)
    frame = int(file.stem.split("_")[1])
    vidwriter.write(img)
    progressBar.update(1)

progressBar.close()
vidwriter.release()
print(f"Wrote {len(files)} frames to '{OUTPUT_FILE}'")

input("Press Enter to continue...")
