from typing import List, Tuple
import math

class LandmarkNormalizer:
    """
    Normalizes hand landmarks to be invariant to hand position and scale.
    """
    @staticmethod
    def normalize(landmarks: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        """
        Applies wrist-relative translation and scale normalization to landmarks.
        
        Args:
            landmarks: List of (x, y, z) tuples for the 21 hand landmarks.
            
        Returns:
            Normalized list of (x', y', z') tuples.
        """
        if not landmarks or len(landmarks) != 21:
            return landmarks
            
        # 1. Wrist-relative translation
        # MediaPipe landmark 0 is the wrist.
        wrist_x, wrist_y, wrist_z = landmarks[0]
        
        translated_landmarks = []
        for x, y, z in landmarks:
            translated_landmarks.append((x - wrist_x, y - wrist_y, z - wrist_z))
            
        # 2. Scale normalization
        # We calculate the maximum distance from the wrist to any other landmark.
        # This makes the features invariant to how close the hand is to the camera.
        max_dist = 0.0
        for tx, ty, tz in translated_landmarks:
            # We use 3D Euclidean distance from the wrist (which is now at 0,0,0)
            dist = math.sqrt(tx**2 + ty**2 + tz**2)
            if dist > max_dist:
                max_dist = dist
                
        # To avoid division by zero if all points are at the wrist (impossible in practice, but safe)
        if max_dist == 0:
            max_dist = 1.0
            
        normalized_landmarks = []
        for tx, ty, tz in translated_landmarks:
            normalized_landmarks.append((tx / max_dist, ty / max_dist, tz / max_dist))
            
        return normalized_landmarks
