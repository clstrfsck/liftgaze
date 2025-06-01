#!/usr/bin/env python3

import cv2

# This script splits a video into frames and saves them with frame numbers and timestamps in the filename.
# The input video file is specified in the INPUT_FILE variable.
# The output frames are saved in the OUTPUT_DIR directory.
# The output filename format is 'frame_<frame_number>_<timestamp>.jpg'.
# The timestamp is in microseconds and is rounded to the nearest microseconds.
from project import OUTPUT_DIR, INPUT_VIDEO_FILE

OUTPUT_DIR.mkdir(exist_ok = True)
for file in OUTPUT_DIR.iterdir():
    if file.is_file():
        file.unlink()

capture = cv2.VideoCapture(INPUT_VIDEO_FILE)
nextFrame = 0
timestamp = 0.0
while (True):

    success, frame = capture.read()

    if success:
        timestamp = capture.get(cv2.CAP_PROP_POS_MSEC)
        cv2.imwrite(OUTPUT_DIR / f'frame_{nextFrame:04}_{round(timestamp * 1000.0):09}.jpg', frame)
        if (nextFrame % 100) == 0:
            print(f"Output frame {nextFrame} at {timestamp:.3f}ms")
        nextFrame = round(capture.get(cv2.CAP_PROP_POS_FRAMES))
    else:
        break

print(f"Total {nextFrame} frames, {timestamp:.3f}ms")
capture.release()
