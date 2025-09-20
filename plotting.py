from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

base_dir = Path(__file__).parent.resolve()
default_output_dir = f"{base_dir}/output"


def plot_waveform_and_spectrogram(time, data, ffts, chunk_duration, title, output_dir=default_output_dir):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(time, data, linewidth=1)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(time[0], time[-1])
    ax1.set_xticks(np.arange(0, time[-1] + 1, 10))
    ax1.grid(True, alpha=0.3)

    freq_axis = ffts[0][0]
    fft_matrix = np.array([fft_mag for _, fft_mag in ffts]).T
    fft_matrix_log = np.log10(fft_matrix + 1e-10)
    time_axis = np.arange(len(ffts)) * chunk_duration + chunk_duration / 2
    ax2.imshow(
        fft_matrix_log,
        aspect="auto",
        origin="lower",
        extent=[time_axis[0], time_axis[-1], freq_axis[0], freq_axis[-1]],
    )
    ax2.set_ylim(0, 400)
    ax2.set_xticks(np.arange(0, time[-1] + 1, 10))
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (Hz)")

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{title.replace(" ", "_").replace("-","_")}.png", dpi=150, bbox_inches="tight")


def plot_audio_with_fft_range(
    time: np.ndarray,
    data: np.ndarray,
    sample_rate: float,
    start_time: float,
    end_time: float,
    fft_fn: callable = None,
    title: str = "Audio fragment with FFT",
    output_dir=default_output_dir
):
    start_idx = int(start_time * sample_rate)
    end_idx = int(end_time * sample_rate)

    start_idx = max(0, start_idx)
    end_idx = min(len(data), end_idx)

    time_range = time[start_idx:end_idx]
    data_range = data[start_idx:end_idx]

    freq, fft_magnitude = fft_fn(data_range, sample_rate)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(time_range, data_range, linewidth=1)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title(f"Audio Signal ({start_time:.1f}s - {end_time:.1f}s)")
    ax1.grid(True, alpha=0.3)

    ax2.plot(freq, fft_magnitude, linewidth=1)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_xlim(0, 400)
    ax2.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()

    filename = f"{output_dir}/{title.replace(" ", "_").replace("-","_")}_{start_time:.1f}s_{end_time:.1f}s.png"
    plt.savefig(filename, dpi=150, bbox_inches="tight")

    return freq, fft_magnitude


def plot_waveform(time: np.ndarray, data:np.ndarray, ranges_to_highlight:list[tuple[int, int]], title:str="test", output_dir=default_output_dir):
    highlighted_time_elements = []
    highlighted_data_elements = []
    non_highlighted_time_elements = []
    non_highlighted_data_elements = []

    curr_idx = 0

    for start, end in ranges_to_highlight:
        non_highlighted_time_elements.extend(time[curr_idx:start])
        non_highlighted_data_elements.extend(data[curr_idx:start])

        highlighted_time_elements.extend(time[start:end])
        highlighted_data_elements.extend(data[start:end])

        curr_idx = end

    if curr_idx < len(time):
        non_highlighted_time_elements.extend(time[curr_idx:])
        non_highlighted_data_elements.extend(data[curr_idx:])

    fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
    ax1.scatter(non_highlighted_time_elements, non_highlighted_data_elements, color='blue', marker='o', label='Other', s=0.01)
    ax1.scatter(highlighted_time_elements, highlighted_data_elements, color='red', marker='o', label='Blast-beats', s=0.01)
    ax1.set_xticks(np.arange(0, time[-1] + 1, 15))
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x // 60)}:{int(x % 60):02d}"))
    ax1.set_xlim(time[0], time[-1])
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{title.replace(" ", "_").replace("-","_")}.png", dpi=150, bbox_inches="tight")
    return fig
