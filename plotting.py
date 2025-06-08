import matplotlib.pyplot as plt
import numpy as np


def plot_waveform_and_spectrogram(time, data, ffts, chunk_duration, title):
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
    ax2.set_ylim(0, 500)
    ax2.set_xticks(np.arange(0, time[-1] + 1, 10))
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Frequency (Hz)")

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(f"./tmp/{title.replace(' ', '_')}.png", dpi=150, bbox_inches="tight")


def plot_audio_with_fft_range(
    time: np.ndarray,
    data: np.ndarray,
    sample_rate: float,
    start_time: float,
    end_time: float,
    fft_fn: callable = None,
    title: str = "Audio fragment with FFT",
):
    start_idx = int(start_time * sample_rate)
    end_idx = int(end_time * sample_rate)

    start_idx = max(0, start_idx)
    end_idx = min(len(data), end_idx)

    time_range = time[start_idx:end_idx]
    data_range = data[start_idx:end_idx]

    freq, fft_magnitude = fft_fn(data_range, sample_rate)

    nyquist_idx = len(freq) // 2
    freq = freq[:nyquist_idx]
    fft_magnitude = fft_magnitude[:nyquist_idx]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.plot(time_range, data_range, linewidth=1)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title(f"Audio Signal ({start_time:.1f}s - {end_time:.1f}s)")
    ax1.grid(True, alpha=0.3)

    ax2.plot(freq, fft_magnitude, linewidth=1)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_xlim(0, 1000)
    ax2.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()

    filename = f"./tmp/{title.replace(' ', '_')}_{start_time:.1f}s-{end_time:.1f}s.png"
    plt.savefig(filename, dpi=150, bbox_inches="tight")
