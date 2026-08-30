import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pathlib import Path
from typing import Tuple, List, Optional, Any

from src.config.settings import MEDIAPIPE_MODEL_PATH

class HandDetector:
    """
    A wrapper around MediaPipe's HandLandmarker Tasks API.
    Provides methods to process static images and video streams.
    """
    def __init__(self, 
                 model_path: str = str(MEDIAPIPE_MODEL_PATH),
                 num_hands: int = 1,
                 min_detection_confidence: float = 0.5,
                 min_presence_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5,
                 running_mode: vision.RunningMode = vision.RunningMode.IMAGE):
        """
        Initializes the HandDetector with MediaPipe HandLandmarker.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"\n[ERROR] MediaPipe model file not found at: {model_path}\n"
                f"Please download the official 'hand_landmarker.task' file from:\n"
                f"https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task\n"
                f"and place it in the 'models/' directory."
            )

        self.running_mode = running_mode
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=self.running_mode,
            num_hands=num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_presence_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect_image(self, image_bgr: np.ndarray) -> Optional[Any]:
        """
        Detects hand landmarks in a static BGR image.
        Returns the HandLandmarkerResult or None.
        """
        if self.running_mode != vision.RunningMode.IMAGE:
            raise ValueError("Detector is not initialized in IMAGE running mode.")
            
        # Convert BGR to RGB as required by MediaPipe
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        detection_result = self.detector.detect(mp_image)
        return detection_result

    def detect_video(self, image_bgr: np.ndarray, timestamp_ms: int) -> Optional[Any]:
        """
        Detects hand landmarks in a BGR video frame at the given timestamp.
        """
        if self.running_mode != vision.RunningMode.VIDEO:
            raise ValueError("Detector is not initialized in VIDEO running mode.")
            
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        detection_result = self.detector.detect_for_video(mp_image, timestamp_ms)
        return detection_result

    def extract_features(self, detection_result: Any, image_width: int, image_height: int) -> Tuple[List[Tuple[float, float, float]], Optional[str], Optional[Tuple[int, int, int, int]]]:
        """
        Extracts 21 landmarks, handedness, and calculates a bounding box from the detection result.
        Only processes the first detected hand.
        """
        if not detection_result or not detection_result.hand_landmarks:
            return [], None, None

        # Take the first hand
        landmarks = detection_result.hand_landmarks[0]
        handedness = detection_result.handedness[0][0].category_name
        
        # Format landmarks as list of (x, y, z)
        landmark_list = [(lm.x, lm.y, lm.z) for lm in landmarks]
        
        # Calculate bounding box
        x_coords = [lm.x * image_width for lm in landmarks]
        y_coords = [lm.y * image_height for lm in landmarks]
        
        x_min, x_max = int(min(x_coords)), int(max(x_coords))
        y_min, y_max = int(min(y_coords)), int(max(y_coords))
        
        # Add some padding to the bounding box
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(image_width, x_max + padding)
        y_max = min(image_height, y_max + padding)
        
        bbox = (x_min, y_min, x_max, y_max)
        
        return landmark_list, handedness, bbox

    def draw_landmarks(self, image_bgr: np.ndarray, detection_result: Any) -> np.ndarray:
        """
        Utility to draw landmarks and bounding box on a copy of the image.
        """
        annotated_image = image_bgr.copy()
        
        if not detection_result or not detection_result.hand_landmarks:
            return annotated_image
            
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),        # Index
            (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
            (9, 13), (13, 14), (14, 15), (15, 16), # Ring
            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
        ]
        
        height, width, _ = annotated_image.shape
        
        for hand_landmarks, handedness in zip(detection_result.hand_landmarks, detection_result.handedness):
            # Convert normalized landmarks to pixel coordinates
            pixel_landmarks = []
            for lm in hand_landmarks:
                px = int(lm.x * width)
                py = int(lm.y * height)
                pixel_landmarks.append((px, py))
                
            # Draw connections
            for connection in connections:
                start_idx, end_idx = connection
                if start_idx < len(pixel_landmarks) and end_idx < len(pixel_landmarks):
                    cv2.line(annotated_image, pixel_landmarks[start_idx], pixel_landmarks[end_idx], (0, 255, 0), 2)
                    
            # Draw points
            for px, py in pixel_landmarks:
                cv2.circle(annotated_image, (px, py), 4, (0, 0, 255), -1)
            
            # Draw bounding box
            _, _, bbox = self.extract_features(detection_result, width, height)
            if bbox:
                x_min, y_min, x_max, y_max = bbox
                cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
                
                label = handedness[0].category_name if isinstance(handedness, list) else handedness.category_name
                cv2.putText(annotated_image, label, (x_min, y_min - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                            
        return annotated_image
