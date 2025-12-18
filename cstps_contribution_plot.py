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

# =============================
# Load data
# =============================
chauhan = pd.read_excel(os.path.join(DATA_DIR, "Chauhan_Colony_2024.xlsx"))
midc = pd.read_excel(os.path.join(DATA_DIR, "MIDC_2024.xlsx"))

# =============================
# Calculate annual mean PM2.5
# =============================
pm_chauhan = chauhan["PM2.5 (ug/m3)"].mean()
pm_midc = midc["PM2.5 (ug/m3)"].mean()

# CSTPS Influence Index
cstps_index = ((pm_midc - pm_chauhan) / pm_chauhan) * 100

# =============================
# Plot
# =============================
plt.figure(figsize=(6,5))
plt.bar(
    ["Chauhan Colony\n(Residential)", "MIDC\n(Near CSTPS)"],
    [pm_chauhan, pm_midc]
)

plt.ylabel("Annual Average PM2.5 (µg/m³)")
plt.title("Impact of CSTPS on PM2.5 Levels (2024)")

# Annotation
plt.text(
    0.5,
    max(pm_chauhan, pm_midc) * 0.95,
    f"MIDC is {cstps_index:.1f}% higher than Chauhan Colony",
    ha="center",
    fontsize=10
)

plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "CSTPS_PM25_Contribution.png"), dpi=300)
plt.show()
