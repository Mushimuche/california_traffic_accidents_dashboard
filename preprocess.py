# import polars as pl
# import time

# # --- CONFIGURATION ---
# input_file = "usa_accidents_dataset/US_Accidents_March23.csv"
# output_file = "us_accidents_strict_clean.csv" # Saving as strict version

# print(f"--- Processing {input_file} (Strict Mode) ---")
# start_time = time.time()

# try:
#     # 1. Setup Lazy Scan
#     q_raw = pl.scan_csv(input_file, ignore_errors=True)
    
#     # Get original count for comparison
#     total_rows_raw = q_raw.select(pl.len()).collect().item()
#     print(f"Original Row Count: {total_rows_raw:,}")

#     # 2. Define Columns to Drop ENTIRELY (The ones that are truly useless)
#     # Note: We are KEEPING End_Lat/End_Lng this time
#     cols_to_drop_entirely = [
#         "ID", "Source", "Description", "Country", "Zipcode", "Airport_Code",
#         "Wind_Chill(F)", "Precipitation(in)", "Civil_Twilight", 
#         "Nautical_Twilight", "Astronomical_Twilight", "Timezone", "Weather_Timestamp"
#     ]

#     # 3. Build the Cleaning Query
#     q_clean = (
#         q_raw
#         .drop(cols_to_drop_entirely) 
        
#         # FIX DATES
#         .with_columns([
#             pl.col("Start_Time").str.to_datetime(),
#             pl.col("End_Time").str.to_datetime()
#         ])
        
#         # DROP ROWS based on your specific request
#         # 1. Drop if End_Lat OR End_Lng is missing (This removes ~3.4M rows)
#         .drop_nulls(subset=["End_Lat", "End_Lng"])
        
#         # 2. Drop if other critical info is missing (Temp, Weather, City)
#         .drop_nulls(subset=["Temperature(F)", "Weather_Condition", "Sunrise_Sunset", "City", "Street"])
        
#         # FEATURE ENGINEERING (Add these now so they are ready for the dashboard)
#         .with_columns([
#             pl.col("Start_Time").dt.hour().alias("Hour"),
#             pl.col("Start_Time").dt.month().alias("Month"),
#             pl.col("Start_Time").dt.weekday().alias("Weekday"),
#             ((pl.col("End_Time") - pl.col("Start_Time")).dt.total_minutes()).alias("Duration_Minutes")
#         ])
        
#         # FILL NULLS (Only for things that are safe to guess)
#         .with_columns(pl.col("Wind_Speed(mph)").fill_null(0))
#     )

#     # 4. Execute & Save
#     print("\nStreaming strict data to CSV... (This will drop ~50% of data)")
#     q_clean.sink_csv(output_file)
    
#     # 5. Verify Results
#     print(f"Saved to: {output_file}")
    
#     # Check how many remain
#     q_final = pl.scan_csv(output_file)
#     total_rows_clean = q_final.select(pl.len()).collect().item()
    
#     rows_dropped = total_rows_raw - total_rows_clean
#     percent_dropped = (rows_dropped / total_rows_raw) * 100

#     print("-" * 40)
#     print(f"Original Rows: {total_rows_raw:,}")
#     print(f"Cleaned Rows:  {total_rows_clean:,}")
#     print(f"Rows Dropped:  {rows_dropped:,} ({percent_dropped:.2f}%)")
#     print("-" * 40)
#     print(f"Total time: {time.time() - start_time:.2f} seconds")

# except Exception as e:
#     print(f"\nERROR: {e}")

import polars as pl
import time

# Input: Your strict cleaned dataset
input_file = "us_accidents_strict_clean.csv"
output_file = "us_accidents_ca_only.csv"

print("--- Filtering Data for California (CA) Only ---")
start_time = time.time()

try:
    # 1. Scan the full dataset
    q = pl.scan_csv(input_file)

    # 2. Filter for CA
    # This is the only line you need to change to pick a different state
    ca_q = q.filter(pl.col("State") == "CA")

    # 3. Count the rows
    total_ca_rows = ca_q.select(pl.len()).collect().item()
    
    # Get total US rows for comparison
    total_us_rows = q.select(pl.len()).collect().item()
    percent = (total_ca_rows / total_us_rows) * 100


    print(f"Total US Accidents:      {total_us_rows:,}")
    print(f"Total CA Accidents:      {total_ca_rows:,}")
    print(f"California Share:        {percent:.2f}% of all data")

    # 4. Save the CA-only file
    print(f"\nSaving CA dataset to {output_file}...")
    ca_q.sink_csv(output_file)
    print("Success!")
    
    print(f"Time taken: {time.time() - start_time:.2f} seconds")

except Exception as e:
    print(f"ERROR: {e}")