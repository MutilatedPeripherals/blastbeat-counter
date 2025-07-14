import shutil
from pathlib import Path

import demucs.separate
import librosa
import numpy as np


def extract_drums(input_file_path: Path) -> tuple[np.ndarray, np.ndarray, float]:
    if not input_file_path.exists():
        raise FileNotFoundError(f"The input file {input_file_path.as_posix()} does not exist.")

    extracted_drums_file_path = input_file_path.parent / f"{input_file_path.stem}_drums.wav"

    if not extracted_drums_file_path.exists():
        temp_file_path = (
                input_file_path.parent / "htdemucs" / f"{input_file_path.stem}" / "drums.wav"
        )
        print("Isolating drums with Demucs...")
        demucs.separate.main(
            ["--two-stems", "drums", "--device", "cuda", "-o", "input", input_file_path.as_posix()]
        )
        shutil.copy(temp_file_path, extracted_drums_file_path)
        shutil.rmtree(temp_file_path.parent)

    y, sample_rate = librosa.load(extracted_drums_file_path, mono=True)
    time = np.arange(len(y)) / sample_rate

    return time, y.astype(np.float32), sample_rate


if __name__ == "__main__":
    base_dir = Path(__file__).parent.resolve()

    file_path = Path(f"{base_dir}/input/Eloy Casagrande - Manipulation of Tragedy Sepultura - Live Session.mp3")
    extract_drums(file_path)