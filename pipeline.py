import argparse
import csv
from pathlib import Path

from downloading import download_from_youtube_as_mp3
from processing import process_song

parser = argparse.ArgumentParser()
parser.add_argument("csv_path", type=Path)
args = parser.parse_args()

with open(args.csv_path, newline="") as f:
    reader = csv.DictReader(line for line in f if not line.lstrip().startswith("#"))
    rows = [row for row in reader if row.get("src")]

for row in rows:
    src = row["src"].strip()
    band_width = float(row["band_width"]) if row.get("band_width") else None
    threshold = float(row["threshold"]) if row.get("threshold") else None
    step_size = (
        float(row["step_size_in_seconds"]) if row.get("step_size_in_seconds") else None
    )

    if src.startswith("http://") or src.startswith("https://"):
        print(f"Processing YouTube URL: {src}")
        success, file_path = download_from_youtube_as_mp3(src)
        if not success or not file_path:
            print(f"Failed to download: {src}")
            continue
    else:
        file_path = Path(src)
        if not file_path.exists():
            print(f"File does not exist: {file_path}")
            continue

    kwargs = {}
    if band_width is not None:
        kwargs["band_width"] = band_width
    if threshold is not None:
        kwargs["threshold"] = threshold
    if step_size is not None:
        kwargs["step_size_in_seconds"] = step_size

    process_song(file_path, **kwargs)
    print("-----")
