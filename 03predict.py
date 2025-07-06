#!/usr/bin/env python3

from ultralytics import YOLO
from pathlib import Path
from tqdm import tqdm
import json
import logging

from files import images_in_dir
from project import YOLO_TRAIN_DIR, OUTPUT_DIR, CONFIDENCE_THRESHOLD

# Make logging a bit quieter
logger = logging.getLogger("ultralytics")
logger.setLevel(logging.ERROR)

model = YOLO(YOLO_TRAIN_DIR / f"weights/best.pt")

files = images_in_dir(OUTPUT_DIR)
files.sort(key=lambda x: int(x.stem.split("_")[1]))  # Sort by frame number

progressBar = tqdm(total=len(files), desc="Predicting frames", unit="frame")
for file in files:
    results = model.predict(file, save = True, conf = CONFIDENCE_THRESHOLD, line_width = 1, verbose = False)
    data = []
    for r in results:
        names = r.names
        clss = r.boxes.cls
        xyxys = r.boxes.xyxy
        for i in range(len(clss)):
            cls = int(clss[i])
            x1, y1, x2, y2 = xyxys[i]
            d = {
                "frame": file.name,
                "class": names[cls],
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2)
            }
            data.append(d)
    jsonOutput = (Path(results[0].save_dir) / file.name).with_suffix(".json")
    with open(jsonOutput, "w") as f:
        json.dump(data, f, indent = 4)
    progressBar.update(1)

progressBar.close()
print(f"Predicted {len(files)} files from '{OUTPUT_DIR}'")

input("Press Enter to continue...")
