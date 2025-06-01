from pathlib import Path

# The name of this project, used for file naming.
# Change this to match your project name.
PROJECT_NAME = "example"

# You will need three files in this directory:
# - <project>.mp4: The video file to process
# - <project>.tsv: The gaze points file
# - <project>.yaml: The model configuration file (if applicable)
# You shouldn't need to change this.
INPUT_DIR = Path("input")

# The input video file.  Any video that OpenCV can read should work.
# You should only need to change this if you have a different format
# video file.
INPUT_VIDEO_FILE = INPUT_DIR / f"{PROJECT_NAME}.mp4"

# Output frames are written into this directory in step 00split.py.
# You probably don't need to change this unless you have a specific reason.
OUTPUT_DIR = Path("output_frames")

# Output directory for training and validation frames.
# Step 01sample.py will randomly select frames from OUTPUT_DIR
# You should need to change this.
TRAIN_DIR = Path("train")

# Count of images to sample for training and validation.
# You probably want ~8 frames for training and ~2 for validation.
# You will need to discard frames that have no target features, and
# ideally you should have a mix of frames with target features in a
# range of poses you want to detect.
SAMPLE_COUNT = 12

# YOLO training output is written here.
# If you change this, you will also need to change the code to match.
YOLO_TRAIN_DIR = Path(f"runs/train/yolo11-{PROJECT_NAME}")

# Number of epochs to train the model.
# The larger this is, the better the model will be, but it will take longer.
TRAIN_EPOCHS = 500

# YOLO validation output is written here.
# This code doesn't use this directly, but you should manually check the
# validation results.
# If you change this, you will also need to change the code to match.
YOLO_VAL_DIR = Path(f"runs/train/yolo11-{PROJECT_NAME}2")

# YOLO prediction output is written here.
# If you change this, you will also need to change the code to match.
YOLO_PREDICT_DIR = Path("runs/detect/predict")
