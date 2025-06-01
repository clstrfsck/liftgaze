#!/usr/bin/env python3

from files import OUTPUT_DIR

directories = [ OUTPUT_DIR ]

for dir in directories:
    dir.mkdir(exist_ok = True)
    print(f"Deleting all files in '{dir}'")
    for file in dir.iterdir():
        if file.is_file():
            file.unlink()
