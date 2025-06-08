import os

import librosa
import numpy as np

from plotting import plot_audio_with_fft


def read_mp3(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    data, sample_rate = librosa.load(file_path, sr=None, mono=True)
    time = np.arange(len(data)) / sample_rate

    return time, data, sample_rate


def get_fft(x: np.ndarray, sample_rate: float):
    from numpy.fft import fft

    X = fft(x)
    N = len(X)
    n = np.arange(N)
    T = N / sample_rate
    freq = n / T

    return freq, np.abs(X)


if __name__ == "__main__":
    file_path = "./media/Dying Fetus - Subjected To A Beating.mp3"
    time, data, sample_rate = read_mp3(file_path)
    freq, fft_magnitude = get_fft(data, sample_rate)
    plot_audio_with_fft(
        time, data, sample_rate, freq, fft_magnitude, title=os.path.basename(file_path)
    )
