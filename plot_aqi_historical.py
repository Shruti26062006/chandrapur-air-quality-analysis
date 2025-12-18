import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.dates as mdates

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
# Date conversion
# =============================
df["From Date"] = pd.to_datetime(df["From Date"], dayfirst=True)

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
# Monthly aggregation
# =============================
df["Month"] = df["From Date"].dt.to_period("M")
df_monthly = df.groupby(["Month", "Station"])[pollutants].mean().reset_index()
df_monthly["Month"] = df_monthly["Month"].dt.to_timestamp()

# =============================
# AQI calculation (simplified)
# =============================
def calc_aqi(row):
    aqi_pm25 = row["PM2.5"] * (100 / 60)
    aqi_pm10 = row["PM10"] * (100 / 100)
    aqi_no2  = row["NO2"]  * (100 / 80)
    aqi_so2  = row["SO2"]  * (100 / 80)
    aqi_co   = row["CO"]   * (100 / 2)
    aqi_o3   = row["Ozone"]* (100 / 100)
    return max(aqi_pm25, aqi_pm10, aqi_no2, aqi_so2, aqi_co, aqi_o3)

df_monthly["AQI"] = df_monthly.apply(calc_aqi, axis=1)

# =============================
# Plotting
# =============================
all_plots = pollutants + ["AQI"]
fig, axes = plt.subplots(len(all_plots), 1, figsize=(15, 4*len(all_plots)))

for i, param in enumerate(all_plots):
    ax = axes[i]

    sns.lineplot(
        data=df_monthly,
        x="Month",
        y=param,
        hue="Station",
        marker="o",
        ax=ax
    )

    # AQI bands
    if param == "AQI":
        ax.axhspan(0, 50, alpha=0.2)
        ax.axhspan(51, 100, alpha=0.2)
        ax.axhspan(101, 200, alpha=0.2)
        ax.axhspan(201, 300, alpha=0.2)
        ax.axhspan(301, 500, alpha=0.2)
        ax.set_ylabel("AQI")

    ax.set_title(f"{param} – Monthly Comparison (2024)")
    ax.set_xlabel("Month")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
out_file = os.path.join(PLOT_DIR, "Chandrapur_Monthly_Pollutants_AQI_2024.png")
plt.savefig(out_file, dpi=300)
plt.show()

print("Plot saved at:", out_file)

