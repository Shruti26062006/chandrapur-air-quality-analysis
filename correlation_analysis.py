import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# =============================
# Paths
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
PLOT_DIR = os.path.join(BASE_DIR, "..", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

chauhan_file = os.path.join(DATA_DIR, "Chauhan_Colony_2024.xlsx")
midc_file = os.path.join(DATA_DIR, "MIDC_2024.xlsx")

# =============================
# Load data
# =============================
df1 = pd.read_excel(chauhan_file)
df2 = pd.read_excel(midc_file)

df1["Station"] = "Chauhan Colony"
df2["Station"] = "MIDC"

df = pd.concat([df1, df2], ignore_index=True)

# =============================
# Rename columns
# =============================
df = df.rename(columns={
    "PM2.5 (ug/m3)": "PM2.5",
    "PM10 (ug/m3)": "PM10",
    "NO2 (ug/m3)": "NO2",
    "SO2 (ug/m3)": "SO2",
    "CO (mg/m3)": "CO",
    "Ozone (ug/m3)": "Ozone"
})

pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone"]

# =============================
# Correlation plots per station
# =============================
for station in df["Station"].unique():
    df_station = df[df["Station"] == station][pollutants]

    corr = df_station.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )
    plt.title(f"Pollutant Correlation – {station} (2024)")
    plt.tight_layout()

    out_file = os.path.join(
        PLOT_DIR,
        f"Correlation_{station.replace(' ', '_')}_2024.png"
    )
    plt.savefig(out_file, dpi=300)
    plt.show()

    print(f"Correlation plot saved for {station}")
