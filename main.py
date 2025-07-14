from pathlib import Path

import numpy as np
from numpy.fft import fft

from extraction import extract_drums
from plotting import plot_audio_with_fft_range


def do_fft(x: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    X = fft(x)
    N = len(X)
    n = np.arange(N)
    T = N / sample_rate
    freq = n / T

    # Only keep positive frequencies
    nyquist_idx = len(freq) // 2
    freq = freq[:nyquist_idx]
    X = X[:nyquist_idx]

    return freq, np.abs(X)


threshold = 37.6


def is_peak_present_around_frequency(freq_to_find:float, freq: np.ndarray, fft_magnitude: np.ndarray, band_width:float=10., threshold = 37.6) -> bool:
    lower_bound = freq_to_find - band_width
    upper_bound = freq_to_find + band_width

    # Martins approach:  sum intensities (proxy for area under the curve), and compare with a trheshold -> if meets thresh, it contains a peak around the freq. we a re looking for

    indexes = np.where((freq >= lower_bound) & (freq <= upper_bound))[0]
    if len(indexes) == 0:
        return False

    intensity_sum = np.sum(fft_magnitude[indexes])

    return intensity_sum > threshold


if __name__ == "__main__":
    base_dir = "/home/linomp/Downloads"
    default_output_dir = f"./output"

    file_path = Path(f"{base_dir}/Dying Fetus - Subjected To A Beating.wav")
    time, data, sample_rate = extract_drums(file_path)

    song_name = file_path.stem
    freq, fft_magnitude  = plot_audio_with_fft_range(
        time, data, sample_rate, 29, 29.2, do_fft, title=f"{song_name} | Bass drum isolation example",
        output_dir=default_output_dir
    )

    bass_drum_freq = 60.0
    peak_present = is_peak_present_around_frequency(bass_drum_freq, freq, fft_magnitude, band_width=5.0)

    print(f"Bass drum present ({bass_drum_freq} Hz): {peak_present}")