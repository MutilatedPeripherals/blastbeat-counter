import shutil
import warnings
from pathlib import Path

import demucs.separate
import librosa
import numpy as np

# TODO: fix; perhaps coming from htdemucs or librosa
warnings.filterwarnings("ignore", message="Torchaudio's I/O functions now support per-call backend dispatch")


def read_audio_file(input_file_path: Path) -> tuple[np.ndarray, np.ndarray, float]:
    y, sample_rate = librosa.load(input_file_path, mono=True)
    time = np.arange(len(y)) / sample_rate

    return time, y.astype(np.float32), sample_rate


def extract_drums(input_file_path: Path, skip_cache=False) -> tuple[tuple[np.ndarray, np.ndarray, float], Path]:
    if not input_file_path.exists():
        raise FileNotFoundError(f"The input file {input_file_path.as_posix()} does not exist.")

    extracted_drums_file_path = input_file_path.parent / f"{input_file_path.stem}_drums.wav"

    if skip_cache or not extracted_drums_file_path.exists():
        print("Extracting drums")
        temp_file_path = (
                input_file_path.parent / "htdemucs" / f"{input_file_path.stem}" / "drums.wav"
        )
        print("Isolating drums with Demucs...")
        demucs.separate.main(
            ["--two-stems", "drums", "--device", "cuda", "-o", f"{input_file_path.parent}", input_file_path.as_posix()]
        )
        shutil.copy(temp_file_path, extracted_drums_file_path)
        shutil.rmtree(temp_file_path.parent)

    return read_audio_file(extracted_drums_file_path), extracted_drums_file_path


if __name__ == "__main__":
    base_dir = "/home/linomp/Downloads"

    file_path = Path(f"{base_dir}/Dying Fetus - Subjected To A Beating.wav")
    extract_drums(file_path)