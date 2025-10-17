import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np

base_dir = Path(__file__).parent.resolve()
default_output_dir = f"{base_dir}/output"


def save_result(
    time: np.ndarray,
    ranges_to_highlight: list[tuple[int, int]],
    snare_frequency: float,
    bass_drum_frequency: float,
    filepath: Path,
    drumtrack_path: Path,
    output_dir: str = default_output_dir,
):
    output = {
        "blast_beats": [],
        "snare_frequency": snare_frequency,
        "bass_drum_frequency": bass_drum_frequency,
    }

    for start, end in ranges_to_highlight:
        output["blast_beats"].append(
            {"start_time": float(time[start]), "end_time": float(time[end - 1])}
        )

    zip_path = f"{output_dir}/{filepath.stem.replace(' ', '_').replace('-', '_')}.zip"
    with ZipFile(zip_path, "w") as zipf:
        zipf.writestr(
            f"{filepath.stem.replace(' ', '_').replace('-', '_')}.json",
            json.dumps(output, indent=4),
        )
        zipf.write(filepath, arcname=filepath.name)
        zipf.write(drumtrack_path, arcname=drumtrack_path.name)

    print(f"Exported zip with audio, drumtrack, and JSON to: {zip_path}")
    return zip_path
