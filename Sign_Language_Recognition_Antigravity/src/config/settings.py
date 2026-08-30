import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Dataset paths
DATASET_DIR = BASE_DIR / "dataset"
RAW_DATA_DIR = DATASET_DIR / "raw" / "asl_alphabet_train"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
WEBCAM_DATA_DIR = DATASET_DIR / "webcam"

# Models directory
MODELS_DIR = BASE_DIR / "models"
MEDIAPIPE_MODEL_PATH = MODELS_DIR / "hand_landmarker.task"

# Outputs directory
OUTPUTS_DIR = BASE_DIR / "outputs"
METRICS_DIR = OUTPUTS_DIR / "metrics"
PLOTS_DIR = OUTPUTS_DIR / "plots"
DETECTION_OUTPUT_DIR = OUTPUTS_DIR / "hand_detection"

# MediaPipe configuration
MP_NUM_HANDS = 1
MP_MIN_DETECTION_CONFIDENCE = 0.5
MP_MIN_PRESENCE_CONFIDENCE = 0.5
MP_MIN_TRACKING_CONFIDENCE = 0.5

# Ensure output directories exist
DETECTION_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Real-Time Application Settings
CAMERA_INDEX = 0
MIN_CONFIDENCE_THRESHOLD = 0.6
SMOOTHING_WINDOW_SIZE = 10
MIN_STABLE_FRAMES = 6
COOLDOWN_FRAMES = 20
IMAGE_INFERENCE_INTERVAL = 3  # Run image model every 3 frames
TARGET_IMG_SIZE = (224, 224)
CLASS_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']
