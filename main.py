import os

import librosa
import numpy as np
from numpy.fft import fft

from plotting import plot_waveform_and_spectrogram


def read_audio_file(file_path: str) -> tuple[np.ndarray, np.ndarray, float]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    data, sample_rate = librosa.load(file_path, sr=None, mono=True)
    time = np.arange(len(data)) / sample_rate

    return time, data, sample_rate


def do_fft(x: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    X = fft(x)
    N = len(X)
    n = np.arange(N)
    T = N / sample_rate
    freq = n / T

    return freq, np.abs(X)


if __name__ == "__main__":
    file_path = "./media/Dying Fetus - Subjected To A Beating.wav"
    time, data, sample_rate = read_audio_file(file_path)

    ffts = []
    chunk_duration = 1
    chunk_size = sample_rate * chunk_duration

    for i in range(0, len(data), chunk_size):
        chunk = data[i : i + chunk_size]
        if len(chunk) < chunk_size:
            break

        freq, fft_values = do_fft(chunk, sample_rate)

        # Only keep positive frequencies
        nyquist_idx = len(fft_values) // 2
        freq = freq[:nyquist_idx]
        fft_values = fft_values[:nyquist_idx]

        ffts.append((freq, fft_values))

    plot_waveform_and_spectrogram(
        time, data, ffts, chunk_duration, title=file_path.replace("./media/", "")
    )
