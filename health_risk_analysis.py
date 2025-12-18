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
df = df.rename(columns={"PM2.5 (ug/m3)": "PM2.5"})

# =============================
# Standards
# =============================
WHO_LIMIT = 5
CPCB_LIMIT = 40

# =============================
# Risk metrics
# =============================
summary = []

for station in df["Station"].unique():
    sub = df[df["Station"] == station]

    avg_pm25 = sub["PM2.5"].mean()
    unsafe_days = (sub["PM2.5"] > CPCB_LIMIT).sum()

    summary.append({
        "Station": station,
        "Average PM2.5": avg_pm25,
        "Unsafe Days (>40 µg/m³)": unsafe_days,
        "Times WHO Limit": avg_pm25 / WHO_LIMIT
    })

risk_df = pd.DataFrame(summary)
print(risk_df)

# =============================
# Plot
# =============================
plt.figure(figsize=(7,5))
plt.bar(risk_df["Station"], risk_df["Average PM2.5"])
plt.axhline(CPCB_LIMIT, linestyle="--", label="CPCB Limit (40)")
plt.axhline(WHO_LIMIT, linestyle=":", label="WHO Guideline (5)")
plt.ylabel("Average PM2.5 (µg/m³)")
plt.title("Health Risk Indicator – PM2.5 (2024)")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(PLOT_DIR, "Health_Risk_PM25.png"), dpi=300)
plt.show()
