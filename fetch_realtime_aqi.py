import requests
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")

os.makedirs(DATA_FOLDER, exist_ok=True)

# CPCB / AQI India style endpoint (used by CPCB dashboard)
URL = "https://api.waqi.info/feed/{}/?token=demo"

stations = {
    "Chauhan_Colony_Chandrapur": "chandrapur",
    "MIDC_Chandrapur": "chandrapur"
}


# -----------------------------
# Fetch Data
# -----------------------------
records = []

for station, query in stations.items():
    try:
        response = requests.get(URL.format(query), timeout=10)
        data = response.json()

        if data["status"] != "ok":
            print(f"Data not available for {station}")
            continue

        iaqi = data["data"].get("iaqi", {})

        record = {
            "timestamp": datetime.now(),
            "station": station,
            "PM2.5": iaqi.get("pm25", {}).get("v"),
            "PM10": iaqi.get("pm10", {}).get("v"),
            "SO2": iaqi.get("so2", {}).get("v"),
            "NO2": iaqi.get("no2", {}).get("v"),
            "CO": iaqi.get("co", {}).get("v"),
            "O3": iaqi.get("o3", {}).get("v"),
            "AQI": data["data"].get("aqi")
        }

        records.append(record)
        print(f"Fetched data for {station}")

    except Exception as e:
        print(f"Error fetching {station}: {e}")

# -----------------------------
# Save CSV
# -----------------------------
df = pd.DataFrame(records)

filename = f"{DATA_FOLDER}/chandrapur_realtime_aqi.csv"
df.to_csv(filename, index=False)

print("Data saved to:", filename)
