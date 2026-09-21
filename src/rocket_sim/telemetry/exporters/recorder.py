import csv
from pathlib import Path


def record_telemetry(data: dict):
    save_dir = Path("telemetry_data") 
    save_dir.mkdir(parents=True, exist_ok=True)
    csv_path = save_dir / "telemetry.csv"

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

        writer.writerow(data)