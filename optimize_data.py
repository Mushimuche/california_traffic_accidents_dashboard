import pandas as pd
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

# These are the ONLY columns your app and training script actually need.
COLS_TO_KEEP = [
    # Core Data
    'Severity', 'Start_Time', 
    
    # Location (Used for Map)
    'Start_Lat', 'Start_Lng', 'City', 
    
    # Weather (Used for Filters & Prediction)
    'Weather_Condition', 'Temperature(F)', 'Humidity(%)',
    
    # POIs (Used for 'Impact of Road Features' Plot & Prediction)
    'Junction', 'Crossing', 'Traffic_Signal', 'Stop', 
    'Station', 'Amenity', 'Bump', 'Give_Way', 
    'No_Exit', 'Roundabout'
]

FILES_TO_OPTIMIZE = [
    "us_accidents_ca_only.csv",
    "us_accidents_ca_balanced.csv"
]

# =============================================================================
# OPTIMIZATION LOGIC
# =============================================================================

def optimize_file(file_path):
    print(f"Processing {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"  -> File not found. Skipping.")
        return

    try:
        # 1. Read only the necessary columns (Drastically reduces memory usage)
        # We use strict=False in case one file is missing a column (like City)
        # but generally, we want to intersect with available columns.
        
        # Peek at columns first to avoid errors if a file is missing 'City' etc.
        available_cols = pd.read_csv(file_path, nrows=0).columns.tolist()
        final_cols = [c for c in COLS_TO_KEEP if c in available_cols]
        
        df = pd.read_csv(file_path, usecols=final_cols)
        
        # 2. Print Stats
        original_size = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  -> Original size: {original_size:.2f} MB")
        
        # 3. Overwrite the file
        df.to_csv(file_path, index=False)
        
        new_size = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  -> Optimized size: {new_size:.2f} MB")
        print(f"  -> Reduction: {original_size - new_size:.2f} MB saved!")

    except Exception as e:
        print(f"  -> Error optimizing {file_path}: {e}")

if __name__ == "__main__":
    print("Starting Dataset Optimization...")
    for file in FILES_TO_OPTIMIZE:
        optimize_file(file)
    print("Done. You can now deploy these smaller files.")