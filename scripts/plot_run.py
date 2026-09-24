import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

def get_newest_csv_data():
    curr_dir = Path(__file__).resolve().parent
    telemetry_dir = curr_dir.parent / "telemetry_data"

    csv_files = list(telemetry_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV found at {telemetry_dir}")

    newest_file = max(csv_files, key=lambda f: f.stat().st_mtime)

    return newest_file

def plot_csv_data():
    file = get_newest_csv_data()
    
    df = pd.read_csv(file)

    x_data = df['t']
    y_data = df['y']

    plt.figure(figsize=(10, 6))

    plt.plot(x_data, y_data)

    plt.xlabel("Mission time (s)", fontweight="bold")
    plt.ylabel("Altitude (m)", fontweight="bold")
    plt.title(f"Flight Data for: {file.name}")
    plt.grid(True)

    out = Path(__file__).resolve().parent.parent / "docs" / f"flight_data_{file.stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(out, dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    plot_csv_data()