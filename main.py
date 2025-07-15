from pathlib import Path

import numpy as np
from numpy.fft import fft

from extraction import extract_drums
from plotting import plot_waveform


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


def is_peak_present_around_frequency(freq_to_find:float, freq: np.ndarray, fft_magnitude: np.ndarray, band_width:float=10., threshold = 37.6) -> bool:
    lower_bound = freq_to_find - band_width
    upper_bound = freq_to_find + band_width

    # Martins approach:  sum intensities (proxy for area under the curve), and compare with a trheshold -> if meets thresh, it contains a peak around the freq. we a re looking for

    indexes = np.where((freq >= lower_bound) & (freq <= upper_bound))[0]
    if len(indexes) == 0:
        return False

    intensity_sum = np.sum(fft_magnitude[indexes])

    return intensity_sum > threshold

def contains_snare_or_bass_drum(freq: np.ndarray, fft_magnitude: np.ndarray, bass_drum_freq: float = 50.0, snare_drum_freq: float = 300.0) -> tuple[bool, bool]:
    snare_present = is_peak_present_around_frequency(snare_drum_freq, freq, fft_magnitude, band_width=10.0)
    bass_drum_present = is_peak_present_around_frequency(bass_drum_freq, freq, fft_magnitude, band_width=10.0)

    return snare_present, bass_drum_present

def analyze_song(time, data, sample_rate)-> list[tuple[tuple[int, int], bool, bool]]:
    results = []

    step_size_in_seconds = 0.1
    step_size_in_samples = int(step_size_in_seconds * sample_rate)

    for start_idx in range(0, len(time), step_size_in_samples):
        end_idx = start_idx + step_size_in_samples
        data_range = data[start_idx:end_idx]

        freq, fft_magnitude = do_fft(data_range, sample_rate)
        snare_present, bass_drum_present = contains_snare_or_bass_drum(freq, fft_magnitude)
        results.append(((start_idx, end_idx), snare_present, bass_drum_present))

    return results

def identify_blasts(sections: list[tuple[float, bool, bool]]) -> list[tuple[int,int]]:
    pass

if __name__ == "__main__":
    base_dir = "/home/linomp/Downloads"
    default_output_dir = f"./output"

    file_path = Path(f"{base_dir}/Dying Fetus - Subjected To A Beating.wav")
    time, data, sample_rate = extract_drums(file_path)

    results = analyze_song(time, data, sample_rate)
    for idx, snare, bass in results:
        print(f"({idx}) - Snare: {snare}, Bass: {bass}")

    blast_ranges = [(int(1e6), int(3e6)), (int(4e6), int(5e6))]
    plot_waveform(time, data, blast_ranges, title=file_path.stem)