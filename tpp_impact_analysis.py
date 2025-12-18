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
    "SO2 (ug/m3)": "SO2",
    "NO2 (ug/m3)": "NO2"
})

# =============================
# Correlation analysis
# =============================
corr_data = df[["PM2.5", "SO2", "NO2"]].corr()
print("Correlation Matrix:\n", corr_data)

# =============================
# Scatter plots
# =============================
plt.figure()
plt.scatter(df["SO2"], df["PM2.5"])
plt.xlabel("SO₂ (µg/m³)")
plt.ylabel("PM2.5 (µg/m³)")
plt.title("PM2.5 vs SO₂ (TPP influence)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "PM25_vs_SO2.png"), dpi=300)
plt.show()

plt.figure()
plt.scatter(df["NO2"], df["PM2.5"])
plt.xlabel("NO₂ (µg/m³)")
plt.ylabel("PM2.5 (µg/m³)")
plt.title("PM2.5 vs NO₂ (Combustion signature)")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "PM25_vs_NO2.png"), dpi=300)
plt.show()
