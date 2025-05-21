#!/usr/bin/env python3

import random
import shutil
from dirs import images_in_dir

TRAIN_COUNT = 12
from dirs import OUTPUT_DIR, TRAIN_DIR

TRAIN_DIR.mkdir(exist_ok = True)
for file in TRAIN_DIR.iterdir():
    if file.is_file():
        raise ValueError(f"The directory '{TRAIN_DIR}' is not empty. Please remove the files before running the script.")

files = images_in_dir(OUTPUT_DIR)
if len(files) < TRAIN_COUNT:
    raise ValueError(f"The directory '{OUTPUT_DIR}' contains fewer than {TRAIN_COUNT} files ({len(files)}).")

random.shuffle(files)
for i in range(TRAIN_COUNT):
    file = files[i]
    dst = TRAIN_DIR / file.name
    shutil.copy2(file, dst)
    print(f"Copied {file} to {dst}")

print(f"Copied {TRAIN_COUNT} files from '{OUTPUT_DIR}' to '{TRAIN_DIR}'.")
