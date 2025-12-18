import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

chauhan = pd.read_excel(os.path.join(DATA_DIR, "Chauhan_Colony_2024.xlsx"))
midc = pd.read_excel(os.path.join(DATA_DIR, "MIDC_2024.xlsx"))

chauhan_pm = chauhan["PM2.5 (ug/m3)"].mean()
midc_pm = midc["PM2.5 (ug/m3)"].mean()

cstps_index = ((midc_pm - chauhan_pm) / chauhan_pm) * 100

print("Average PM2.5 – Chauhan Colony:", round(chauhan_pm, 2))
print("Average PM2.5 – MIDC:", round(midc_pm, 2))
print("CSTPS Influence Index (%):", round(cstps_index, 1))
