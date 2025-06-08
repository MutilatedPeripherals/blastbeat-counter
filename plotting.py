import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots


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
    fig = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.1,
    )

    fig.add_trace(
        go.Scatter(
            x=time, y=data, mode="lines", name="Audio Signal", line=dict(width=1)
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=freq,
            y=fft_magnitude,
            mode="lines",
            name="FFT Magnitude",
            line=dict(width=1),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(title=title, height=800, showlegend=False)
    fig.update_xaxes(title_text="Time (s)", row=1, col=1)
    fig.update_yaxes(title_text="Amplitude", row=1, col=1)
    fig.update_xaxes(title_text="Frequency (Hz)", row=2, col=1)
    fig.update_yaxes(title_text="Magnitude", row=2, col=1)
    plot(fig, filename=f"./tmp/{title.replace(' ', '_')}.html", auto_open=True)
