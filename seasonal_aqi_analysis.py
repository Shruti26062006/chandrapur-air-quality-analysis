import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
# Date handling
# =============================
df["From Date"] = pd.to_datetime(df["From Date"], dayfirst=True)
df["Month"] = df["From Date"].dt.month

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

# =============================
# Assign seasons
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

pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone"]

# =============================
# Seasonal averages
# =============================
df_seasonal = df.groupby(["Season", "Station"])[pollutants].mean().reset_index()

# =============================
# Plot
# =============================
fig, axes = plt.subplots(3, 2, figsize=(14, 14))
axes = axes.flatten()

for i, param in enumerate(pollutants):
    sns.barplot(
        data=df_seasonal,
        x="Season",
        y=param,
        hue="Station",
        ax=axes[i]
    )
    axes[i].set_title(f"{param} – Seasonal Variation")
    axes[i].set_xlabel("Season")
    axes[i].set_ylabel(param)

plt.tight_layout()
out_file = os.path.join(PLOT_DIR, "Seasonal_Pollutant_Comparison_2024.png")
plt.savefig(out_file, dpi=300)
plt.show()

print("Seasonal plot saved at:", out_file)
