import pandas as pd
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
# Load Data
# =============================
df1 = pd.read_excel(chauhan_file)
df2 = pd.read_excel(midc_file)

df1["Station"] = "Chauhan Colony"
df2["Station"] = "MIDC"

df = pd.concat([df1, df2], ignore_index=True)

# =============================
# Date processing
# =============================
df["From Date"] = pd.to_datetime(df["From Date"], dayfirst=True)
df["Month"] = df["From Date"].dt.month

# =============================
# Season mapping
# =============================
def season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["Season"] = df["Month"].apply(season)

# =============================
# Rename pollutant
# =============================
df = df.rename(columns={"PM2.5 (ug/m3)": "PM2.5"})

# =============================
# Seasonal average
# =============================
seasonal_avg = (
    df.groupby(["Station", "Season"])["PM2.5"]
    .mean()
    .reset_index()
)

print(seasonal_avg)

# =============================
# Plot
# =============================
plt.figure(figsize=(8, 6))

for station in seasonal_avg["Station"].unique():
    sub = seasonal_avg[seasonal_avg["Station"] == station]
    plt.plot(sub["Season"], sub["PM2.5"], marker="o", label=station)

plt.ylabel("Average PM2.5 (µg/m³)")
plt.title("Seasonal Variation of PM2.5 – Chandrapur (2024)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(PLOT_DIR, "Seasonal_PM25_2024.png"), dpi=300)
plt.show()
