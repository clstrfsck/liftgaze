#!/usr/bin/env python3

from ultralytics import YOLO
from pathlib import Path
import json

from dirs import OUTPUT_DIR, images_in_dir

model = YOLO("runs/train/yolo11-lift/weights/best.pt")

files = images_in_dir(OUTPUT_DIR)
files.sort(key=lambda x: int(x.stem.split("_")[1]))  # Sort by frame number

for file in files:
    results = model.predict(file, save = True, conf = 0.25, line_width = 1, verbose = False)
    data = []
    for r in results:
        names = r.names
        clss = r.boxes.cls
        xywhs = r.boxes.xywh
        for i in range(len(clss)):
            cls = int(clss[i])
            x, y, w, h = xywhs[i]
            d = {
                "frame": file.name,
                "class": names[cls],
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
            }
            data.append(d)
    jsonOutput = (Path(results[0].save_dir) / file.name).with_suffix(".json")
    with open(jsonOutput, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Predicted {file}")

print(f"Predicted {len(files)} files from '{OUTPUT_DIR}'")
