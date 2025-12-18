import pandas as pd
import os

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")

input_file = os.path.join(DATA_FOLDER, "chandrapur_realtime_aqi.csv")
output_file = os.path.join(DATA_FOLDER, "chandrapur_aqi_cleaned.csv")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(input_file)
print("Initial data:")
print(df)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# For now, keep NaN as is (we will explain missing data later)
df_clean = df.copy()

# Save cleaned data
df_clean.to_csv(output_file, index=False)
print("\nCleaned data saved successfully at:", output_file)
