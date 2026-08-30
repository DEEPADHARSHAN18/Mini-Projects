import os
import cv2
import pandas as pd
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

from src.config.settings import RAW_DATA_DIR, DATASET_DIR, METRICS_DIR
from src.detection.hand_detector import HandDetector
from src.landmarks.normalizer import LandmarkNormalizer
from src.landmarks.feature_builder import FeatureBuilder

class LandmarkExtractor:
    def __init__(self, output_file: str = "landmarks.csv"):
        self.output_path = DATASET_DIR / "landmarks" / output_file
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("Initializing Hand Detector...")
        self.detector = HandDetector()
        
    def extract_dataset(self, test_mode: bool = False, samples_per_class: int = 5):
        """
        Extracts landmarks from the dataset.
        If test_mode is True, only processes up to `samples_per_class` images per class.
        Resumes extraction if the output CSV already exists.
        """
        if not RAW_DATA_DIR.exists():
            print(f"Error: Dataset directory {RAW_DATA_DIR} not found.")
            return

        classes = [d for d in RAW_DATA_DIR.iterdir() if d.is_dir()]
        
        # Load already processed files if resuming
        processed_files = set()
        write_header = True
        
        if self.output_path.exists():
            try:
                # Read just the image_path column to know what's processed
                existing_df = pd.read_csv(self.output_path, usecols=['image_path'])
                processed_files = set(existing_df['image_path'].tolist())
                write_header = False
                print(f"Resuming extraction. Found {len(processed_files)} previously processed valid images.")
            except Exception as e:
                print(f"Could not read existing CSV for resuming: {e}. Starting fresh.")
                write_header = True
                
        # Stats tracking
        stats = defaultdict(lambda: {'total': 0, 'detected': 0})
        
        # Open file in append mode
        mode = 'w' if write_header else 'a'
        
        with open(self.output_path, mode, newline='') as csvfile:
            for cls_dir in classes:
                cls_name = cls_dir.name
                images = list(cls_dir.glob("*.jpg"))
                
                if test_mode:
                    images = images[:samples_per_class]
                    
                print(f"Processing class: {cls_name} ({len(images)} images)")
                
                # Batch list to write to CSV
                batch_features = []
                
                for img_path in tqdm(images, desc=cls_name, leave=False):
                    img_name_rel = f"{cls_name}/{img_path.name}"
                    
                    stats[cls_name]['total'] += 1
                    
                    if img_name_rel in processed_files:
                        stats[cls_name]['detected'] += 1
                        continue
                        
                    image = cv2.imread(str(img_path))
                    if image is None:
                        continue
                        
                    # Detect
                    result = self.detector.detect_image(image)
                    landmarks, handedness, _ = self.detector.extract_features(result, image.shape[1], image.shape[0])
                    
                    if landmarks:
                        stats[cls_name]['detected'] += 1
                        
                        # Normalize
                        norm_landmarks = LandmarkNormalizer.normalize(landmarks)
                        
                        # Build features
                        features = FeatureBuilder.build_features(
                            norm_landmarks, cls_name, handedness, img_name_rel
                        )
                        
                        batch_features.append(features)
                
                # Append batch to CSV
                if batch_features:
                    df_batch = pd.DataFrame(batch_features)
                    df_batch.to_csv(csvfile, header=write_header, index=False)
                    write_header = False  # Only write header once
                    
                    # Add to processed files so we don't recount in the same run if interrupted
                    processed_files.update([f['image_path'] for f in batch_features])

        self._generate_report(stats)

    def _generate_report(self, stats: dict):
        report_data = []
        
        total_images = 0
        total_detected = 0
        
        hand_classes_total = 0
        hand_classes_detected = 0
        
        for cls_name, data in stats.items():
            total = data['total']
            detected = data['detected']
            not_detected = total - detected
            pct = (detected / total * 100) if total > 0 else 0
            
            total_images += total
            total_detected += detected
            
            if cls_name != 'nothing':
                hand_classes_total += total
                hand_classes_detected += detected
                
            report_data.append({
                'Class': cls_name,
                'Total images': total,
                'Hand detected': detected,
                'Hand not detected': not_detected,
                'Detection percentage': f"{pct:.2f}%"
            })
            
        df_report = pd.DataFrame(report_data)
        report_path = METRICS_DIR / "landmark_extraction_report.csv"
        df_report.to_csv(report_path, index=False)
        
        raw_rate = (total_detected / total_images * 100) if total_images > 0 else 0
        hand_rate = (hand_classes_detected / hand_classes_total * 100) if hand_classes_total > 0 else 0
        
        print("\n" + "="*50)
        print("LANDMARK EXTRACTION REPORT")
        print("="*50)
        print(f"Total images processed: {total_images}")
        print(f"Valid landmark rows:    {total_detected}")
        print(f"Failed hand detections: {total_images - total_detected}")
        print(f"Nothing images:         {stats.get('nothing', {}).get('total', 0)}")
        print(f"Raw detection rate:     {raw_rate:.2f}%")
        print(f"Hand-class det. rate:   {hand_rate:.2f}% (excluding 'nothing')")
        
        print("\nSpecific Classes of Interest:")
        for cls_name in ['M', 'N', 'A', 'nothing', 'space']:
            if cls_name in stats:
                pct = (stats[cls_name]['detected'] / stats[cls_name]['total'] * 100) if stats[cls_name]['total'] > 0 else 0
                print(f"  - {cls_name}: {pct:.2f}% ({stats[cls_name]['detected']}/{stats[cls_name]['total']})")
                
        # Validate output shape
        if self.output_path.exists():
            df_out = pd.read_csv(self.output_path)
            num_features = df_out.shape[1] - 3  # minus image_path, class, handedness
            print(f"\nOutput file path:       {self.output_path}")
            print(f"Number of features:     {num_features} (Expected 63)")
            if df_out.isnull().values.any():
                print("WARNING: NaN values found in output CSV!")
            else:
                print("Verified: No NaN values in output CSV.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="Run full extraction instead of test mode")
    args = parser.parse_args()
    
    extractor = LandmarkExtractor(output_file="landmarks.csv" if args.full else "test_landmarks.csv")
    if args.full:
        print("Running FULL extraction...")
        extractor.extract_dataset(test_mode=False)
    else:
        print("Running SMALL TEST extraction...")
        extractor.extract_dataset(test_mode=True, samples_per_class=5)
