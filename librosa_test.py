import os
import pickle

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile


def isolate_drums(file_path: str, debug=False) -> np.ndarray:
    cache_file = file_path.replace(".wav", "_cache.pkl")

    if os.path.exists(cache_file):
        print(f"Loading data from pickle file: {cache_file}")
        with open(cache_file, "rb") as f:
            drums, sample_rate = pickle.load(f)
        return drums, sample_rate

    y, sample_rate = librosa.load(file_path, sr=None, mono=True)
    drums = librosa.effects.percussive(y, margin=5)

    if debug:
        output_file = file_path.replace(".wav", "_drums.wav")
        soundfile.write(output_file, drums, sample_rate)

    with open(cache_file, "wb") as f:
        pickle.dump((drums, sample_rate), f)

    return drums, sample_rate


def plot_spectrogram(y: np.ndarray, sample_rate: int, start: float, end: float):
    y_segment = y[int(start * sample_rate) : int(end * sample_rate)]
    S = np.abs(librosa.stft(y_segment, n_fft=512))

    fig, ax = plt.subplots()
    img = librosa.display.specshow(
        librosa.amplitude_to_db(S, ref=np.max),
        y_axis="log",
        x_axis="time",
        ax=ax,
        sr=sample_rate,
        n_fft=512,
        x_coords=np.linspace(start, end, S.shape[1]),
    )
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.savefig(
        f"./tmp/librosa_test/spectrogram_{start}_{end}.png",
        dpi=150,
        bbox_inches="tight",
    )


if __name__ == "__main__":
    file_path = "./media/Dying Fetus - Subjected To A Beating.wav"

    drums, sample_rate = isolate_drums(file_path, debug=True)

    plot_spectrogram(drums, sample_rate, start=29, end=30.9)
    plot_spectrogram(drums, sample_rate, start=32, end=34)
