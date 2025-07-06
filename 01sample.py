#!/usr/bin/env python3

import random
import shutil
from files import images_in_dir

from project import OUTPUT_DIR, TRAIN_DIR, SAMPLE_COUNT

TRAIN_DIR.mkdir(exist_ok = True)
for file in TRAIN_DIR.iterdir():
    if file.is_file():
        raise ValueError(f"The directory '{TRAIN_DIR}' is not empty. Please remove the files before running the script.")

files = images_in_dir(OUTPUT_DIR)
if len(files) < SAMPLE_COUNT:
    raise ValueError(f"The directory '{OUTPUT_DIR}' contains fewer than {SAMPLE_COUNT} files ({len(files)}).")

random.shuffle(files)
for i in range(SAMPLE_COUNT):
    file = files[i]
    dst = TRAIN_DIR / file.name
    shutil.copy2(file, dst)
    print(f"Copied {file} to {dst}")

print(f"Copied {SAMPLE_COUNT} files from '{OUTPUT_DIR}' to '{TRAIN_DIR}'.")

input("Press Enter to continue...")
