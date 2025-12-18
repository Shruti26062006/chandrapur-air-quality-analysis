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
    "PM10 (ug/m3)": "PM10",
    "NO2 (ug/m3)": "NO2",
    "SO2 (ug/m3)": "SO2"
})

# =============================
# CPCB Standards
# =============================
standards = {
    "PM2.5": 60,
    "PM10": 100,
    "NO2": 80,
    "SO2": 80
}

# =============================
# Exceedance calculation
# =============================
results = []

for station in df["Station"].unique():
    df_station = df[df["Station"] == station]

    for pollutant, limit in standards.items():
        exceed_days = (df_station[pollutant] > limit).sum()
        total_days = df_station[pollutant].count()
        percent = (exceed_days / total_days) * 100

        results.append({
            "Station": station,
            "Pollutant": pollutant,
            "Exceedance Days": exceed_days,
            "Percentage (%)": percent
        })

exceed_df = pd.DataFrame(results)
print(exceed_df)

# =============================
# Plot
# =============================
plt.figure(figsize=(10, 6))

for station in exceed_df["Station"].unique():
    sub = exceed_df[exceed_df["Station"] == station]
    plt.bar(
        sub["Pollutant"] + " (" + station + ")",
        sub["Exceedance Days"],
        label=station
    )

plt.ylabel("Number of Exceedance Days (2024)")
plt.title("CPCB Exceedance Days – Chandrapur (2024)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(PLOT_DIR, "Exceedance_Days_2024.png"), dpi=300)
plt.show()
# =============================
# Save Exceedance Table
# =============================
exceed_csv = os.path.join(DATA_DIR, "Exceedance_Summary_2024.csv")
exceed_df.to_csv(exceed_csv, index=False)

print("Exceedance summary saved at:", exceed_csv)
