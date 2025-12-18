import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")
PLOT_FOLDER = os.path.join(BASE_DIR, "..", "plots")
os.makedirs(PLOT_FOLDER, exist_ok=True)

input_file = os.path.join(DATA_FOLDER, "chandrapur_aqi_cleaned.csv")

# -----------------------------
# Load cleaned data
# -----------------------------
df = pd.read_csv(input_file)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Create a readable timestamp for plotting
df["time_str"] = df["timestamp"].dt.strftime('%Y-%m-%d %H:%M')

# -----------------------------
# Filter only PM2.5 and PM10
# -----------------------------
df_pm = df[["time_str", "station", "PM2.5", "PM10"]]

# -----------------------------
# Plotting function
# -----------------------------
def plot_pollutant(pollutant):
    plt.figure(figsize=(10,5))
    sns.lineplot(
        data=df_pm,
        x="time_str",
        y=pollutant,
        hue="station",
        marker="o"
    )
    plt.title(f"{pollutant} Comparison: Chauhan Colony vs MIDC")
    plt.xlabel("Timestamp")
    plt.ylabel(f"{pollutant} (µg/m³)")
    plt.xticks(rotation=45)
    plt.tigh
