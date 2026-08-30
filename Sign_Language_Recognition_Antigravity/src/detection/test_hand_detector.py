import os
import cv2
from pathlib import Path

from src.config.settings import RAW_DATA_DIR, DETECTION_OUTPUT_DIR
from src.detection.hand_detector import HandDetector

def test_hand_detection_on_dataset():
    print("Initializing Hand Detector...")
    try:
        detector = HandDetector()
    except Exception as e:
        print(e)
        return

    # Select representative classes to test
    classes_to_test = ['A', 'M', 'N', 'nothing', 'space']
    samples_per_class = 5
    
    total_images = 0
    successful_detections = 0
    failed_detections = 0
    
    print(f"\nTesting {samples_per_class} samples from classes: {classes_to_test}")
    
    for cls in classes_to_test:
        cls_dir = RAW_DATA_DIR / cls
        if not cls_dir.exists():
            print(f"Directory not found for class: {cls}")
            continue
            
        images = list(cls_dir.glob("*.jpg"))[:samples_per_class]
        
        for img_path in images:
            total_images += 1
            image = cv2.imread(str(img_path))
            
            if image is None:
                print(f"Failed to read image: {img_path}")
                failed_detections += 1
                continue
                
            # Detect
            result = detector.detect_image(image)
            landmarks, handedness, bbox = detector.extract_features(result, image.shape[1], image.shape[0])
            
            img_name = img_path.name
            if landmarks:
                successful_detections += 1
                print(f"[{cls}] {img_name}: DETECTED ({len(landmarks)} landmarks) - {handedness}")
                
                # Visualize and save
                annotated_img = detector.draw_landmarks(image, result)
                save_path = DETECTION_OUTPUT_DIR / f"annotated_{cls}_{img_name}"
                cv2.imwrite(str(save_path), annotated_img)
            else:
                failed_detections += 1
                print(f"[{cls}] {img_name}: NO HAND DETECTED")
                # Save failure case for investigation
                save_path = DETECTION_OUTPUT_DIR / f"failed_{cls}_{img_name}"
                cv2.imwrite(str(save_path), image)

    print("\n" + "="*40)
    print("DETECTION RESULTS")
    print("="*40)
    print(f"Total Images Tested:    {total_images}")
    print(f"Successful Detections:  {successful_detections}")
    print(f"Failed Detections:      {failed_detections}")
    if total_images > 0:
        rate = (successful_detections / total_images) * 100
        print(f"Detection Rate:         {rate:.2f}%")
        
    print(f"\nCheck '{DETECTION_OUTPUT_DIR}' for visualized results and failure cases.")

if __name__ == "__main__":
    test_hand_detection_on_dataset()
