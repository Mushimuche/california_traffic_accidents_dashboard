import pandas as pd

# Load your big CSV with full columns
df = pd.read_csv("us_accidents_ca_only.csv")

# Save as Parquet (requires pyarrow or fastparquet installed)
# pip install pyarrow
df.to_parquet("us_accidents_ca_only.parquet", index=False)