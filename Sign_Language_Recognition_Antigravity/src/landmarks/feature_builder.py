from typing import List, Tuple, Dict, Any

class FeatureBuilder:
    """
    Converts normalized 3D landmarks into a flat feature vector suitable for classical ML models.
    """
    @staticmethod
    def build_features(normalized_landmarks: List[Tuple[float, float, float]], 
                       class_label: str, 
                       handedness: str, 
                       source_image: str) -> Dict[str, Any]:
        """
        Builds a dictionary containing exactly 63 numeric features for the 21 landmarks,
        along with metadata.
        
        Args:
            normalized_landmarks: List of (x, y, z) for 21 points.
            class_label: The ground truth class (e.g. 'A').
            handedness: 'Left' or 'Right' or 'Unknown'.
            source_image: Path or filename of the source image.
            
        Returns:
            A dictionary where keys 'x0'...'z20' are the features, plus metadata keys.
        """
        features: Dict[str, Any] = {
            'image_path': source_image,
            'class': class_label,
            'handedness': handedness
        }
        
        if not normalized_landmarks or len(normalized_landmarks) != 21:
            # Return empty features if no valid landmarks
            return features
            
        # Flatten 21 * 3 = 63 features
        for i, (x, y, z) in enumerate(normalized_landmarks):
            features[f'x{i}'] = x
            features[f'y{i}'] = y
            features[f'z{i}'] = z
            
        return features
