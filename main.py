from pathlib import Path

import numpy as np
from numpy.fft import fft

from extraction import extract_drums
from plotting import plot_audio_with_fft_range, plot_waveform_and_spectrogram

base_dir = Path(__file__).parent.resolve()
default_output_dir = f"{base_dir}/output"


def do_fft(x: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    X = fft(x)
    N = len(X)
    n = np.arange(N)
    T = N / sample_rate
    freq = n / T

    return freq, np.abs(X)


if __name__ == "__main__":
    file_path = Path(f"{base_dir}/input/Dying Fetus - Subjected To A Beating.wav")
    time, data, sample_rate = extract_drums(file_path)

    print("Generating spectrograms...")
    song_name = file_path.stem
    plot_audio_with_fft_range(
        time, data, sample_rate, 29, 30.9, do_fft, title=f"{song_name} | Blast-beat segment example",
        output_dir=default_output_dir
    )
    plot_audio_with_fft_range(
        time, data, sample_rate, 32, 34, do_fft, title=f"{song_name} | Non blast-beat segment example",
        output_dir=default_output_dir
    )

    ffts = []
    chunk_duration = 1
    chunk_size = sample_rate * chunk_duration

    for i in range(0, len(data), chunk_size):
        chunk = data[i: i + chunk_size]
        if len(chunk) < chunk_size:
            break

        freq, fft_values = do_fft(chunk, sample_rate)

        # Only keep positive frequencies
        nyquist_idx = len(fft_values) // 2
        freq = freq[:nyquist_idx]
        fft_values = fft_values[:nyquist_idx]

        ffts.append((freq, fft_values))

    plot_waveform_and_spectrogram(
        time, data, ffts, chunk_duration, title=song_name, output_dir=default_output_dir
    )
