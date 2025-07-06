#!/usr/bin/env python3

from ultralytics import YOLO
from project import PROJECT_NAME, INPUT_DIR, TRAIN_EPOCHS
import logging

# Load a model
model = YOLO("yolo11n.pt")

# Model configuration.
yaml_file = INPUT_DIR / f"{PROJECT_NAME}.yaml"

# Make logging a bit quieter
logger = logging.getLogger("ultralytics")
logger.setLevel(logging.ERROR)

# Train the model
results = model.train(data = yaml_file, epochs = TRAIN_EPOCHS, project = "runs/train", name = f"yolo11-{PROJECT_NAME}")
print(results)

# Evaluate the model
results = model.val(data = yaml_file)
print(results)

input("Press Enter to continue...")
