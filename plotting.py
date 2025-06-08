import matplotlib.pyplot as plt


def plot_audio_with_fft(
    time, data, sample_rate, freq, fft_magnitude, title="Audio Signal with FFT"
):
    # Downsample if data is too large -> TODO remove this maybe?
    if len(data) > 100000:
        step = len(data) // 50000
        time = time[::step]
        data = data[::step]
        downsampled_data = data
    else:
        downsampled_data = data

    nyquist_idx = len(freq) // 2
    freq = freq[:nyquist_idx]
    fft_magnitude = fft_magnitude[:nyquist_idx]

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot audio signal
    ax1.plot(time, data, linewidth=1)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    # Plot FFT magnitude
    ax2.plot(freq, fft_magnitude, linewidth=1)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.grid(True, alpha=0.3)

    # Overall title
    fig.suptitle(title, fontsize=14)
    plt.tight_layout()

    # Save and show
    filename = f"./tmp/{title.replace(' ', '_')}.png"
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.show()
