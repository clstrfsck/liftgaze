#!/usr/bin/env python3

from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Train the model
results = model.train(data = "input/lift.yaml", epochs = 500, project = "runs/train", name = "yolo11-lift")
print(results)

# Evaluate the model
results = model.val(data = "input/lift.yaml")
print(results)
