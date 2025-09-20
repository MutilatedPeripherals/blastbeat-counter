import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np

base_dir = Path(__file__).parent.resolve()
default_output_dir = f"{base_dir}/output"

def save_result(time: np.ndarray, ranges_to_highlight: list[tuple[int, int]], title: Path, output_dir:str=default_output_dir):
    output = {"blast_beats": []}
    for start, end in ranges_to_highlight:
        output["blast_beats"].append({
            "start_time": float(time[start]),
            "end_time": float(time[end-1])
        })
    output["audio_file_path"] = str(title.name)

    zip_path = f"{output_dir}/{title.stem.replace(' ', '_').replace('-', '_')}.zip"
    with ZipFile(zip_path, 'w') as zipf:
        zipf.writestr(f"{title.stem.replace(' ', '_').replace('-', '_')}.json", json.dumps(output, indent=4))
        zipf.write(title, arcname=title.name)

    print(f"Exported zip with audio and JSON to: {zip_path}")
    return zip_path