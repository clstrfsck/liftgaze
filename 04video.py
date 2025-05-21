#!/usr/bin/env python3

import cv2
import pandas as pd

from bisect import bisect_right
from numpy import isfinite
from pathlib import Path

from dirs import images_in_dir

LOOK_FILE = Path('input/lift.tsv')
OUTPUT_FILE = 'lift_predict.mp4'
INPUT_DIR = Path("./runs/detect/predict")

lookPoints = pd.read_csv(LOOK_FILE, sep = '\t')
xPoints = list(lookPoints["Gaze point X"])
yPoints = list(lookPoints["Gaze point Y"])
timestampsUs = list(lookPoints["Recording timestamp"])

files = images_in_dir(INPUT_DIR)
if len(files) == 0:
    raise ValueError(f"No images found in '{INPUT_DIR}'")
files.sort(key=lambda x: int(x.stem.split("_")[1]))  # Sort by frame number

# Get the dimensions of the first image
first_image = cv2.imread(files[0])
image_width = first_image.shape[1]
image_height = first_image.shape[0]
fps = 25  # FIXME: Should read from original video

vidwriter = cv2.VideoWriter(OUTPUT_FILE, cv2.VideoWriter_fourcc(*"mp4v"), fps, (image_width, image_height))
ps = []
for file in files:
    img = cv2.imread(file)
    timestampUs = int(file.stem.split("_")[2])
    ip = bisect_right(timestampsUs, timestampUs)
    (x, y) = (None, None)
    if ip + 1 < len(timestampsUs):
        (t1, t2) = timestampsUs[ip:ip + 2]
        (x1, x2) = xPoints[ip:ip + 2]
        (y1, y2) = yPoints[ip:ip + 2]
        # If we have two sets of points, linearly interpolate the gaze point
        if (isfinite(x1) and isfinite(y1) and isfinite(x2) and isfinite(y2)):
            x = round(x1 + (x2 - x1) * (timestampUs - t1) / (t2 - t1))
            y = round(y1 + (y2 - y1) * (timestampUs - t1) / (t2 - t1))
    ps.append((x, y))
    sz = 10
    for (x, y) in reversed(ps[-sz:]):
        if x and y:
            # Draw a circle at the gaze point
            cv2.circle(img, (x, y), sz, (0, 255, 0), -1)
        sz -= 1
    frame = int(file.stem.split("_")[1])
    if frame % 100 == 0:
        print(f"Writing frame {frame} ({file.name})")
    vidwriter.write(img)

vidwriter.release()
print(f"Wrote {len(files)} frames to '{OUTPUT_FILE}'")
