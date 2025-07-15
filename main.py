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

def analyze_song(time, data, sample_rate)-> list[tuple[float, bool, bool]]:
    results = []

    for start_time in np.arange(0, time[-1], 0.1):
        end_time = start_time + 0.1
        if end_time > time[-1]:
            break

        start_idx = int(start_time * sample_rate)
        end_idx = int(end_time * sample_rate)

        start_idx = max(0, start_idx)
        end_idx = min(len(data), end_idx)

        data_range = data[start_idx:end_idx]

        freq, fft_magnitude = do_fft(data_range, sample_rate)
        result = contains_snare_or_bass_drum(freq, fft_magnitude)
        results.append(result)

    return results

def identify_blasts(sections: list[tuple[float, bool, bool]]) -> list[tuple[float,float]]:
    pass

if __name__ == "__main__":
    base_dir = "/home/linomp/Downloads"
    default_output_dir = f"./output"

    file_path = Path(f"{base_dir}/Dying Fetus - Subjected To A Beating.wav")
    time, data, sample_rate = extract_drums(file_path)

    # song_name = file_path.stem
    # freq, fft_magnitude  = plot_audio_with_fft_range(
    #     time, data, sample_rate, 29, 29.1, do_fft, title=f"{song_name} | Bass drum isolation example",
    #     output_dir=default_output_dir
    # )
    #
    # snare_present, bass_drum_present = contains_snare_or_bass_drum(freq, fft_magnitude)
    # print(f"Snare present: {snare_present}, Bass drum present: {bass_drum_present}")

    results = analyze_song(time, data, sample_rate)
    for i, (snare, bass) in enumerate(results):
        print(f"Time {i * 0.1:.1f}s - Snare: {snare}, Bass: {bass}")

    plot_waveform(time, data, sample_rate, title=file_path.stem)