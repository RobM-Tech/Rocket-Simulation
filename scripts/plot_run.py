import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

def get_newest_csv_data(tag):


    curr_dir = Path(__file__).resolve().parent
    telemetry_dir = curr_dir.parent / "telemetry_data" / f"data{tag}"

    csv_files = list(telemetry_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV found at {telemetry_dir}")

    newest_file = max(csv_files, key=lambda f: f.stat().st_mtime)

    return newest_file

def plot_csv_data(tag):

    file = get_newest_csv_data(tag)
    
    df = pd.read_csv(file)

    time_data = df['t']
    x_data = df["x"]
    y_data = df['y']
    speed_data = df["v_total"]

    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    axes[0].plot(time_data, y_data, linewidth=2)

    axes[0].set_xlabel("Mission time (s)", fontweight="bold")
    axes[0].set_ylabel("Altitude (m)", fontweight="bold")
    axes[0].set_title(f"Climb profile", fontweight="bold")
    axes[0].grid(True)

    axes[1].plot(time_data, speed_data, linewidth=2)

    axes[1].set_xlabel("Mission time (s)", fontweight="bold")
    axes[1].set_ylabel("Speed (v_total)", fontweight="bold")
    axes[1].set_title(f"Energy build-up", fontweight="bold")
    axes[1].grid(True)

    axes[2].plot(x_data, y_data, linewidth=2)

    axes[2].set_xlabel("Downrange (m)", fontweight="bold")
    axes[2].set_ylabel("Altitude (m)", fontweight="bold")
    axes[2].set_title(f"Trajectory shape", fontweight="bold")
    axes[2].grid(True)

    plt.tight_layout()

    out = Path(__file__).resolve().parent.parent / "docs" / f"plot{tag}" / f"flight_data_{file.stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(out, dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    plot_csv_data()