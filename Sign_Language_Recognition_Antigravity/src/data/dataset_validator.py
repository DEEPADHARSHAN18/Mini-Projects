import os
import cv2
import pandas as pd
from collections import defaultdict
from pathlib import Path
import hashlib
from typing import Dict, List, Set, Tuple

class DatasetValidator:
    def __init__(self, raw_data_dir: str = "dataset/raw/asl_alphabet_train"):
        self.raw_data_dir = Path(raw_data_dir)
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        
    def get_file_hash(self, filepath: Path) -> str:
        """Returns the MD5 hash of a file for duplicate detection."""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                # Read in chunks to avoid memory issues with large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    def validate(self, report_path: str = "outputs/metrics/dataset_report.csv"):
        if not self.raw_data_dir.exists():
            print(f"Error: Directory {self.raw_data_dir} does not exist.")
            return
            
        # Detect all subdirectories as classes
        classes = [d for d in self.raw_data_dir.iterdir() if d.is_dir()]
        print(f"Found {len(classes)} classes in {self.raw_data_dir}:\n{[c.name for c in classes]}")
        
        report_data = []
        global_hashes: Dict[str, Path] = {}
        duplicates_found = 0
        total_valid = 0
        
        print("\nInspecting classes (this may take a moment for large datasets)...")
        
        for cls_dir in classes:
            cls_name = cls_dir.name
            files = list(cls_dir.glob('*'))
            
            total_files = len(files)
            valid_images = 0
            invalid_extension = 0
            corrupted_images = 0
            dimensions: Set[str] = set()
            
            for f in files:
                # 1. Extension check
                if f.suffix.lower() not in self.supported_extensions:
                    invalid_extension += 1
                    continue
                
                # 2. Duplicate check (if practical, maybe sampled or full)
                # To make it practical, we hash all files, but we skip hashing if file is unreadable later
                # We will just hash here
                file_hash = self.get_file_hash(f)
                if file_hash:
                    if file_hash in global_hashes:
                        duplicates_found += 1
                    else:
                        global_hashes[file_hash] = f
                
                # 3. Readability & Dimensions check
                try:
                    # using cv2.imread
                    img = cv2.imread(str(f))
                    if img is None:
                        corrupted_images += 1
                    else:
                        valid_images += 1
                        total_valid += 1
                        # shape is (height, width, channels)
                        dim_str = f"{img.shape[1]}x{img.shape[0]}x{img.shape[2] if len(img.shape) > 2 else 1}"
                        dimensions.add(dim_str)
                except Exception:
                    corrupted_images += 1
            
            report_data.append({
                'Class': cls_name,
                'Total': total_files,
                'Valid': valid_images,
                'Invalid_Ext': invalid_extension,
                'Corrupted': corrupted_images,
                'Dimensions': ", ".join(list(dimensions)) if dimensions else "None"
            })
            
        if not report_data:
            print("No data found inside class folders.")
            return
            
        df = pd.DataFrame(report_data)
        
        # Save CSV
        df.to_csv(report_path, index=False)
        print(f"\nReport saved to: {report_path}")
        
        # Display Summary
        print("\n=== Dataset Summary ===")
        print(df.to_string(index=False))
        
        # Check Class Imbalance
        mean_samples = df['Valid'].mean()
        std_samples = df['Valid'].std()
        
        print("\n=== Problems Discovered ===")
        problems_found = False
        
        total_corrupted = df['Corrupted'].sum()
        if total_corrupted > 0:
            print(f"[-!-] Found {total_corrupted} corrupted/unreadable images.")
            problems_found = True
            
        total_invalid_ext = df['Invalid_Ext'].sum()
        if total_invalid_ext > 0:
            print(f"[-!-] Found {total_invalid_ext} files with unsupported extensions.")
            problems_found = True
            
        if duplicates_found > 0:
            print(f"[-!-] Found {duplicates_found} duplicate images across the dataset.")
            problems_found = True
            
        # Arbitrary threshold for imbalance: standard deviation > 20% of mean
        if std_samples > (mean_samples * 0.2):
            print(f"[-!-] Significant class imbalance detected.")
            print(f"      (Std Dev: {std_samples:.2f}, Mean: {mean_samples:.2f})")
            
            # Find min and max
            min_cls = df.loc[df['Valid'].idxmin()]
            max_cls = df.loc[df['Valid'].idxmax()]
            print(f"      Lowest count: {min_cls['Class']} ({min_cls['Valid']})")
            print(f"      Highest count: {max_cls['Class']} ({max_cls['Valid']})")
            problems_found = True
            
        if not problems_found:
            print("[OK] No significant problems discovered.")
            
        print("\n=== Conclusion ===")
        if df['Valid'].sum() == 0:
            print("The dataset has no valid images. NOT ready for Phase 3.")
        else:
            print("The dataset is ready for Phase 3 (MediaPipe hand detection).")

if __name__ == "__main__":
    validator = DatasetValidator()
    validator.validate()
