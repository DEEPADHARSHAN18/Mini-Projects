import cv2
import time
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import mediapipe as mp

from src.detection.hand_detector import HandDetector
from src.landmarks.normalizer import LandmarkNormalizer
from src.recognition.sentence_builder import SentenceBuilder
from src.recognition.smoother import TemporalSmoother
from src.recognition.fusion import PredictionFusion
from src.speech.tts import TTSEngine
from src.config import settings

def main():
    print("Loading models and components...")
    
    # Initialize UI and State components
    sentence_builder = SentenceBuilder()
    smoother = TemporalSmoother(
        window_size=settings.SMOOTHING_WINDOW_SIZE,
        min_stable_frames=settings.MIN_STABLE_FRAMES,
        cooldown_frames=settings.COOLDOWN_FRAMES
    )
    fusion = PredictionFusion(min_confidence=settings.MIN_CONFIDENCE_THRESHOLD)
    tts = TTSEngine()
    normalizer = LandmarkNormalizer()
    
    # Load Hand Detector (VIDEO mode)
    detector = HandDetector(running_mode=mp.tasks.vision.RunningMode.VIDEO)
    
    # Load Landmark Model
    print("Loading Landmark MLP model...")
    landmark_model_path = settings.MODELS_DIR / "landmark" / "MLP_baseline.pkl"
    landmark_model = joblib.load(landmark_model_path)
    
    # Load Image Model
    print("Loading Image MobileNetV2 model...")
    image_model_path = settings.MODELS_DIR / "image" / "asl_mobilenetv2_baseline.keras"
    image_model = tf.keras.models.load_model(image_model_path)
    
    # Open Webcam
    cap = cv2.VideoCapture(settings.CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
        
    print("System ready. Press 'Q' to quit.")
    print("Keybinds: SPACE (add space), BACKSPACE/DEL (delete last), C (clear), T (speak)")
    
    frame_count = 0
    show_debug = True
    last_image_pred = "N/A"
    last_image_conf = 0.0
    
    start_time = time.time()
    fps = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
            
        frame_count += 1
        current_timestamp_ms = int(time.time() * 1000)
        
        # We need a copy of the original frame for image model cropping
        original_frame = frame.copy()
        
        # 1. MediaPipe Hand Detection
        detection_result = detector.detect_video(frame, current_timestamp_ms)
        
        h, w, _ = frame.shape
        landmarks, handedness, bbox = detector.extract_features(detection_result, w, h)
        
        landmark_pred = "nothing"
        landmark_conf = 1.0
        fused_pred = "nothing"
        fused_conf = 1.0
        stable_pred = None
        
        if landmarks:
            # 2. Extract and Normalize Landmarks
            # Ensure it outputs exactly 63 features
            features = normalizer.normalize(landmarks)
            feature_array = np.array(features).reshape(1, -1)
            
            # Predict with Landmark Model
            lm_probs = landmark_model.predict_proba(feature_array)[0]
            lm_pred_idx = np.argmax(lm_probs)
            landmark_pred = landmark_model.classes_[lm_pred_idx]
            landmark_conf = float(lm_probs[lm_pred_idx])
            
            # 3. Image Model Inference (Run every N frames to save CPU)
            if frame_count % settings.IMAGE_INFERENCE_INTERVAL == 0 and bbox is not None:
                x_min, y_min, x_max, y_max = bbox
                # Ensure bbox is within bounds
                x_min, y_min = max(0, x_min), max(0, y_min)
                x_max, y_max = min(w, x_max), min(h, y_max)
                
                # Expand box slightly (e.g. 10%)
                box_w = x_max - x_min
                box_h = y_max - y_min
                padding_x = int(box_w * 0.1)
                padding_y = int(box_h * 0.1)
                
                x_min = max(0, x_min - padding_x)
                y_min = max(0, y_min - padding_y)
                x_max = min(w, x_max + padding_x)
                y_max = min(h, y_max + padding_y)
                
                img_crop = original_frame[y_min:y_max, x_min:x_max]
                
                if img_crop.size > 0:
                    img_crop_resized = cv2.resize(img_crop, settings.TARGET_IMG_SIZE)
                    img_crop_rgb = cv2.cvtColor(img_crop_resized, cv2.COLOR_BGR2RGB)
                    
                    input_tensor = np.expand_dims(img_crop_rgb, axis=0)
                    input_tensor = preprocess_input(input_tensor)
                    
                    # Predict with Image Model
                    img_probs = image_model.predict(input_tensor, verbose=0)[0]
                    img_pred_idx = np.argmax(img_probs)
                    last_image_pred = settings.CLASS_NAMES[img_pred_idx]
                    last_image_conf = float(img_probs[img_pred_idx])
            
            # 4. Fusion
            fused_pred, fused_conf = fusion.fuse(
                landmark_pred, landmark_conf, 
                last_image_pred, last_image_conf
            )
            
            # Draw Landmarks and BBox
            detector.draw_landmarks(frame, detection_result)
            if bbox:
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                cv2.putText(frame, handedness, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            # If no hand, immediately output nothing to break gestures
            fused_pred = "nothing"
            fused_conf = 1.0

        # 5. Temporal Smoothing
        stable_pred = smoother.update(fused_pred, fused_conf)
        
        if stable_pred:
            if stable_pred == "space":
                sentence_builder.add_space()
            elif stable_pred == "del":
                sentence_builder.delete_last()
            else:
                sentence_builder.add_character(stable_pred)
                
        # 6. UI Rendering
        # Top bar for sentence
        cv2.rectangle(frame, (0, 0), (w, 60), (0, 0, 0), -1)
        sentence_str = sentence_builder.get_sentence()
        cv2.putText(frame, sentence_str, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        
        # Calculate FPS
        if frame_count % 10 == 0:
            end_time = time.time()
            fps = 10 / (end_time - start_time)
            start_time = end_time
            
        if show_debug:
            y_offset = 90
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Landmark: {landmark_pred} ({landmark_conf:.2f})", (10, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 100), 2)
            cv2.putText(frame, f"Image   : {last_image_pred} ({last_image_conf:.2f})", (10, y_offset + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
            
            fuse_color = (0, 255, 0) if fused_conf >= settings.MIN_CONFIDENCE_THRESHOLD else (0, 0, 255)
            cv2.putText(frame, f"Fused   : {fused_pred} ({fused_conf:.2f})", (10, y_offset + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, fuse_color, 2)
            
            cooldown = smoother.current_cooldown
            status = f"Stable: {stable_pred if stable_pred else 'Wait'}"
            if cooldown > 0:
                status += f" (Cooldown: {cooldown})"
            cv2.putText(frame, status, (10, y_offset + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
        # Display
        cv2.imshow("Real-Time ASL Recognition", frame)
        
        # Input handling
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            sentence_builder.clear()
        elif key == ord(' '):
            sentence_builder.add_space()
        elif key == 8: # Backspace
            sentence_builder.delete_last()
        elif key == ord('t'):
            tts.speak(sentence_builder.get_sentence())
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
