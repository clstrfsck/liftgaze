#!/usr/bin/env python3

import cv2
from tqdm import tqdm

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

fps = capture.get(cv2.CAP_PROP_FPS)
frameCount = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
durationMs = frameCount / fps * 1000.0

print(f"Video: {width}x{height} @ {fps:.2f} fps, {frameCount} frames / {durationMs:.3f}ms")

nextFrame = 0
progressBar = tqdm(total=frameCount, desc="Extracting frames", unit="frame")
while True:
    success, frame = capture.read()

    if not success:
        break

    timestampUs = round(capture.get(cv2.CAP_PROP_POS_MSEC) * 1000.0)
    cv2.imwrite(OUTPUT_DIR / f'frame_{nextFrame:04}_{timestampUs:09}.jpg', frame)
    nextFrame = round(capture.get(cv2.CAP_PROP_POS_FRAMES))
    progressBar.update(1)

progressBar.close()
print(f"Total {nextFrame} frames processed.")
capture.release()

input("Press Enter to continue...")
