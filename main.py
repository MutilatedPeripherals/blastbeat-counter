from pathlib import Path
from typing import NamedTuple

import numpy as np
from numpy.fft import fft

from downloading import download_from_youtube_as_mp3
from extraction import extract_drums
from plotting import plot_waveform


class LabeledSection(NamedTuple):
    start_idx: int
    end_idx: int
    snare_present: bool
    bass_drum_present: bool


def get_frequency_and_intensity_arrays(audio_data: np.ndarray, sample_rate: float) -> tuple[np.ndarray, np.ndarray]:
    X = fft(audio_data)
    N = len(X)
    n = np.arange(N)
    T = N / sample_rate
    freq = n / T

    # Only keep positive frequencies
    nyquist_idx = len(freq) // 2
    freq = freq[:nyquist_idx]
    X = X[:nyquist_idx]

    return freq, np.abs(X)


def is_peak_present_around_frequency(freq_to_find: float, frequencies: np.ndarray, intensities: np.ndarray, band_width: float = 10., threshold=37.6) -> bool:
    lower_bound = freq_to_find - band_width
    upper_bound = freq_to_find + band_width

    # Martins approach:  sum intensities (proxy for area under the curve), and compare with a threshold -> if meets thresh, it contains a peak around the freq. we're looking for
    indexes = np.where((frequencies >= lower_bound) & (frequencies <= upper_bound))[0]
    if len(indexes) == 0:
        return False

    intensity_sum = np.sum(intensities[indexes])

    return intensity_sum > threshold


def get_sections_labeled_by_percussion_content_from_audio(time, data, sample_rate, bass_drum_freq, snare_drum_freq) -> list[LabeledSection]:
    results = []

    step_size_in_seconds = 0.1  # most important magical constant of the whole project.
    step_size_in_samples = int(step_size_in_seconds * sample_rate)

    for start_idx in range(0, len(time), step_size_in_samples):
        end_idx = start_idx + step_size_in_samples
        data_range = data[start_idx:end_idx]

        freq, fft_magnitude = get_frequency_and_intensity_arrays(data_range, sample_rate)

        snare_present = is_peak_present_around_frequency(snare_drum_freq, freq, fft_magnitude)
        bass_drum_present = is_peak_present_around_frequency(bass_drum_freq, freq, fft_magnitude)

        results.append(LabeledSection(start_idx, end_idx, snare_present, bass_drum_present))

    return results


def identify_blastbeat_intervals(sections: list[LabeledSection]) -> list[tuple[int, int]]:
    # primitive approach:  4 snares+bass in a series at least
    min_hits_threshold = 4
    blastbeat_start_idx = 0
    hits_count = 0
    results = []

    for i in range(0, len(sections)):
        if sections[i].snare_present and sections[i].bass_drum_present:
            if hits_count == 0:
                blastbeat_start_idx = i
            hits_count += 1
        else:
            if hits_count >= min_hits_threshold:
                blastbeat_start = sections[blastbeat_start_idx].start_idx
                blastbeat_end = sections[i].start_idx
                results.append((blastbeat_start, blastbeat_end))
            hits_count = 0

    return results

def identify_bass_and_snare_frequencies(audio_data: np.ndarray, sample_rate: float) -> tuple[float, float]:
    # simple approach: fft over the whole song
    freq, intensities = get_frequency_and_intensity_arrays(audio_data, sample_rate)

    # define ranges to look for
    bass_drum_range = (10, 100)
    snare_range = (170, 600)

    # find the peak in the bass drum range
    bass_drum_idx = np.where((freq >= bass_drum_range[0]) & (freq <= bass_drum_range[1]))[0]
    snare_idx = np.where((freq >= snare_range[0]) & (freq <= snare_range[1]))[0]

    bass_drum_freq, snare_freq = None, None

    if bass_drum_idx.size > 0:
        bass_drum_freq = freq[bass_drum_idx[np.argmax(intensities[bass_drum_idx])]]
    else:
        print("Warning: No bass drum frequency found in the specified range.")

    if snare_idx.size > 0:
        snare_freq = freq[snare_idx[np.argmax(intensities[snare_idx])]]
    else:
        print("Warning: No snare frequency found in the specified range.")

    if bass_drum_freq is None or snare_freq is None:
        raise ValueError("Could not identify bass drum or snare frequencies. Please check the audio file.")

    return bass_drum_freq, snare_freq


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str)
    parser.add_argument("--url", type=str)
    args = parser.parse_args()

    if args.file:
        # Mode 1:  use local file
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"The specified file does not exist: {file_path}")
    elif args.url:
        # Mode 2:  download from YouTube
        success, file_path = download_from_youtube_as_mp3(args.url)
        if not success or file_path is None:
            raise RuntimeError("Failed to download the YouTube video.")
        file_path = Path(file_path)
    else:
        raise ValueError("You must provide either a local file path (--file) or a url to download from YouTube (--url)")

    time, audio_data, sample_rate = extract_drums(file_path)
    bass_drum_freq, snare_freq = identify_bass_and_snare_frequencies(audio_data, sample_rate)
    print(f"Identified bass drum frequency: {bass_drum_freq} Hz, snare frequency: {snare_freq} Hz")

    labeled_sections = get_sections_labeled_by_percussion_content_from_audio(time, audio_data, sample_rate, bass_drum_freq, snare_freq)
    blastbeat_intervals = identify_blastbeat_intervals(labeled_sections)
    plot_waveform(time, audio_data, blastbeat_intervals, title=file_path.stem)