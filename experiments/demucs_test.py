import os
from pathlib import Path

import demucs.separate
import librosa
import matplotlib.pyplot as plt
import numpy as np

base_dir = Path(__file__).parent.resolve()
default_output_dir = f"{base_dir}/output/demucs_test"

def plot_spectrogram(
    y: np.ndarray, sample_rate: int, start: float = 0.0, end: float = None, output_dir=default_output_dir
):
    if end is None:
        end = len(y) / sample_rate

    start = max(0, start)
    end = min(end, len(y) / sample_rate)

    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)

    y_segment = y[start_sample:end_sample]
    S = np.abs(librosa.stft(y_segment))

    fig, ax = plt.subplots()
    librosa.display.specshow(
        librosa.amplitude_to_db(S, ref=np.max),
        y_axis="log",
        x_axis="time",
        ax=ax,
        sr=sample_rate,
    )
    plt.savefig(
        f"{output_dir}/spectrogram_{start}_{end}.png",
        dpi=150,
        bbox_inches="tight",
    )

if __name__ == "__main__":

    if not os.path.isfile(default_output_dir):
        os.makedirs(default_output_dir, exist_ok=True)

    input_file_path = Path(f"{base_dir.parent}/input/Dying Fetus - Subjected To A Beating.wav")
    isolated_drums_file_path = (
        input_file_path.parent / "htdemucs" / f"{input_file_path.stem}/drums.wav"
    )

    print("Isolating drums with Demucs...")
    demucs.separate.main(
        ["--two-stems", "drums", "--device", "cuda", "-o", "input", input_file_path.as_posix()]
    )
    print("Generating spectrograms...")

    y, sample_rate = librosa.load(isolated_drums_file_path, mono=True)
    plot_spectrogram(y, sample_rate, start=29, end=30.9)
    plot_spectrogram(y, sample_rate, start=32, end=34)
    plot_spectrogram(y, sample_rate)