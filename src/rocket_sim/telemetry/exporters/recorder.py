import csv
from datetime import datetime
from pathlib import Path




def generate_path(tag):

    save_dir = Path(__file__).resolve().parents[4] / "telemetry_data" / f"data{tag}"
    save_dir.mkdir(parents=True, exist_ok=True)
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    csv_path = save_dir / f"telemetry_{time_stamp}.csv"

    return csv_path


def record_telemetry(data: dict, csv_path):


    # Get list of fieldnames
    fieldnames = list(data.keys())
    # Check file exsitance
    file_exsits = csv_path.exists()

    with open(csv_path,
              mode='a',
              newline='',
              encoding='utf-8'
              ) as f:
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exsits:
            writer.writeheader()
        rounded_data = {
                k: (round(v, 2)
                if isinstance(v, float)
                else v)
                for k, v in data.items()
                }
        
        writer.writerow(rounded_data)