from typing import Tuple

class PredictionFusion:
    def __init__(self, min_confidence: float = 0.5):
        self.min_confidence = min_confidence
        
    def fuse(self, landmark_pred: str, landmark_conf: float, image_pred: str, image_conf: float) -> Tuple[str, float]:
        """
        Fuses predictions from the Landmark and Image models.
        """
        # 1. Both low confidence -> nothing
        if landmark_conf < self.min_confidence and image_conf < self.min_confidence:
            return "nothing", max(landmark_conf, image_conf)
            
        # 2. Both models agree
        if landmark_pred == image_pred:
            # Boost confidence slightly
            boosted_conf = min(1.0, max(landmark_conf, image_conf) + 0.1)
            return landmark_pred, boosted_conf
            
        # 3. Disagreement -> Confidence check with rules
        
        # Penalty for landmark model predicting 'nothing' (since it only had 1 training sample)
        eff_landmark_conf = 0.0 if landmark_pred == "nothing" else landmark_conf
        
        # If one is much more confident than the other
        if eff_landmark_conf > image_conf + 0.2:
            return landmark_pred, eff_landmark_conf
        elif image_conf > eff_landmark_conf + 0.2:
            return image_pred, image_conf
            
        # 4. Similar confidence -> prefer image model if landmark confidence is weak
        if eff_landmark_conf < 0.75:
            return image_pred, image_conf
            
        # 5. Similar high confidence disagreement -> we will return the one with slightly higher confidence
        # The temporal smoother will likely filter this out if it flickers between the two
        if eff_landmark_conf > image_conf:
            return landmark_pred, eff_landmark_conf
        else:
            return image_pred, image_conf
