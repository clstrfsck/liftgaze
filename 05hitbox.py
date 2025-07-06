#!/usr/bin/env python3

import itertools as it
import json
import pandas as pd

from bisect import bisect_left
from numpy import isfinite

from files import jsons_in_dir
from project import PROJECT_NAME, INPUT_DIR, YOLO_PREDICT_DIR

def hit_any_box(x, y, boxes):
    if x and y and boxes:
        for box in boxes:
            _, _, _, bx1, by1, bx2, by2 = box
            if bx1 <= x < bx2 and by1 <= y < by2:
                return "true"
    return "false"

LOOK_FILE = INPUT_DIR / f"{PROJECT_NAME}.tsv"
OUTPUT_FILE = f"{PROJECT_NAME}_predict.tsv"
SPAN_LENGTH = 1  # Number of frames to average for smoothing, 1 for no smoothing

# Read look points from the TSV file.
lookPoints = pd.read_csv(LOOK_FILE, sep = '\t')
xPoints = list(lookPoints["Gaze point X"].ewm(span = SPAN_LENGTH).mean())
yPoints = list(lookPoints["Gaze point Y"].ewm(span = SPAN_LENGTH).mean())
timestampsUs = list(lookPoints["Recording timestamp"])
if len(xPoints) != len(yPoints) or len(xPoints) != len(timestampsUs):
    raise ValueError("Look points, timestamps, and gaze points must have the same length")
print(f"Read {len(xPoints)} look points from '{LOOK_FILE}'")

# Load all JSON files and extract hitboxes by frame
files = jsons_in_dir(YOLO_PREDICT_DIR)
if len(files) == 0:
    raise ValueError(f"No JSON files found in '{YOLO_PREDICT_DIR}'")
files.sort(key=lambda x: int(x.stem.split("_")[1]))  # Sort by frame number
# Extract frame numbers and times from filenames.
frames = []
for f in files:
    _, frameNumber, frameTime = f.stem.split("_")
    frames.append((int(frameNumber), int(frameTime.removesuffix(".json"))))
hitboxes = []
for f in files:
    with open(f, 'r') as file:
        data = json.load(file)
        for c in data:
            frame = c.get("frame", None)
            cls = c.get("class", None)
            x1 = c.get("x1", None)
            y1 = c.get("y1", None)
            x2 = c.get("x2", None)
            y2 = c.get("y2", None)
            if frame and cls and x1 and y1 and x2 and y2:
                (_, frameNumber, frameTime) = frame.removesuffix(".jpg").split("_")
                hitboxes.append((int(frameNumber), int(frameTime), cls, int(x1), int(y1), int(x2), int(y2)))
            else:
                print(f"Warning: Incomplete data in {f}: {c}")
print(f"Found {len(hitboxes)} hitboxes in {len(files)} files")

# Unique classes in hitboxes.
clss = set()
for h in hitboxes:
    (_, _, cls, _, _, _, _) = h
    clss.add(cls)
clss = sorted(clss)
print(f"Detected {len(clss)} classes: {', '.join(clss)}")

# Group frames by frame number and time.
hitboxFrames = {}
for frameNumber, hbs in it.groupby(hitboxes, lambda x: x[0]):
   hitboxFrames[frameNumber] = list(hbs)

# Write output file:
# - frame number
# - frame time in microseconds
# - for each detection class, whether the gaze point hits any box of that class
# - for each detection class, whether that class has a hitbox in the frame
with open(OUTPUT_FILE, 'w') as out:
    # Write header
    out.write("frame\tframeTime_us")
    for cls in clss:
        out.write(f"\t{cls}_hit")
    for cls in clss:
        out.write(f"\t{cls}_box")
    out.write("\n")
    # Write each frame with hitbox information
    for frameNumber, frameTime in frames:
        out.write(f"{frameNumber}\t{frameTime}")
        # Linear interpolation of gaze points
        (x, y) = (None, None)
        ip = bisect_left(timestampsUs, frameTime)
        if ip > 0:
            (t1, t2) = timestampsUs[ip - 1:ip + 1]
            (x1, x2) = xPoints[ip - 1:ip + 1]
            (y1, y2) = yPoints[ip - 1:ip + 1]
            # If we have two sets of points, linearly interpolate the gaze point
            if isfinite(x1) and isfinite(y1) and isfinite(x2) and isfinite(y2):
                x = round(x1 + (x2 - x1) * (frameTime - t1) / (t2 - t1))
                y = round(y1 + (y2 - y1) * (frameTime - t1) / (t2 - t1))
        boxes = hitboxFrames.get(frameNumber, [])
        boxesByClass = {}
        for cls, box in it.groupby(boxes, lambda x: x[2]):
            boxesByClass[cls] = list(box)
        for cls in clss:
            out.write("\t")
            out.write(hit_any_box(x, y, boxesByClass.get(cls, None)))
        for cls in clss:
            out.write("\t")
            out.write(str(cls in boxesByClass).lower())
        out.write("\n")

print(f"Wrote {len(frames)} frames to '{OUTPUT_FILE}'")

input("Press Enter to continue...")
