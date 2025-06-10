from pathlib import Path

import demucs.separate
import librosa
import matplotlib.pyplot as plt
import numpy as np


def plot_spectrogram(
    y: np.ndarray, sample_rate: int, start: float = 0.0, end: float = None
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
    img = librosa.display.specshow(
        librosa.amplitude_to_db(S, ref=np.max),
        y_axis="log",
        x_axis="time",
        ax=ax,
        sr=sample_rate,
    )
    # fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.savefig(
        f"./tmp/demucs_test/spectrogram_{start}_{end}.png",
        dpi=150,
        bbox_inches="tight",
    )


if __name__ == "__main__":
    file_path = "./media/Dying Fetus - Subjected To A Beating.wav"
    isolated_drums_file_path = file_path.replace("media", "separated/htdemucs").replace(
        ".wav", "/drums.wav"
    )

    if not Path(isolated_drums_file_path).exists():
        print("Isolating drums with Demucs...")
        demucs.separate.main(
            ["--two-stems", "drums", "--jobs", "4", "--device", "cuda", file_path]
        )
    print("Generating spectrograms...")

    y, sample_rate = librosa.load(isolated_drums_file_path, mono=True)

    plot_spectrogram(y, sample_rate, start=29, end=30.9)
    plot_spectrogram(y, sample_rate, start=32, end=34)
    plot_spectrogram(y, sample_rate)
