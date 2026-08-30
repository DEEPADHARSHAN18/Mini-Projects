from collections import deque
from typing import Optional, Tuple
from collections import Counter

class TemporalSmoother:
    def __init__(self, window_size: int, min_stable_frames: int, cooldown_frames: int):
        self.window_size = window_size
        self.min_stable_frames = min_stable_frames
        self.cooldown_frames = cooldown_frames
        
        self.buffer = deque(maxlen=window_size)
        self.current_cooldown = 0
        self.last_committed = None
        
    def update(self, prediction: str, confidence: float) -> Optional[str]:
        """
        Updates the smoothing buffer with a new prediction.
        Returns the committed character if the gesture is stable and cooldown is expired.
        Returns None otherwise.
        """
        # Decrease cooldown
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            
        if not prediction or prediction == "nothing":
            self.buffer.append(None)
            # If nothing is detected, we can reset the last_committed so the user can sign the same letter again
            if len(self.buffer) == self.window_size and all(x is None for x in self.buffer):
                self.last_committed = None
            return None
            
        self.buffer.append(prediction)
        
        # We need enough frames to make a decision
        if len(self.buffer) < self.min_stable_frames:
            return None
            
        # Check if we are in cooldown
        if self.current_cooldown > 0:
            return None
            
        # Get the most common prediction in the recent 'min_stable_frames'
        recent_frames = list(self.buffer)[-self.min_stable_frames:]
        
        # If any of the recent frames are None, it's not a stable gesture
        if None in recent_frames:
            return None
            
        counter = Counter(recent_frames)
        most_common_pred, count = counter.most_common(1)[0]
        
        # Require 100% agreement in the min_stable_frames window for extreme stability
        if count == self.min_stable_frames:
            # Special stability requirement for space and del
            if most_common_pred in ["space", "del"]:
                # Require even more stability (e.g., the whole window size)
                if len(self.buffer) == self.window_size:
                    full_counter = Counter(self.buffer)
                    if full_counter[most_common_pred] < self.window_size - 2:
                        return None
                else:
                    return None
                    
            if most_common_pred != self.last_committed:
                self.last_committed = most_common_pred
                self.current_cooldown = self.cooldown_frames
                self.buffer.clear()
                return most_common_pred
                
        return None
