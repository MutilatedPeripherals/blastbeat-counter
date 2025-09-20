import streamlit as st
from streamlit_player import st_player

from downloading import download_from_youtube_as_mp3
from extraction import extract_drums
from plotting import plot_waveform
from processing import get_sections_labeled_by_percussion_content_from_audio, identify_bass_and_snare_frequencies, \
    identify_blastbeat_intervals

options = {
    "events": ["onProgress"],
    "progress_interval": 500
}

def process_song(url: str, progress_bar, debug_container):
    debug_container.markdown("Processing started")
    progress_bar.progress(10)

    success, file_path = download_from_youtube_as_mp3(url)
    if not success or file_path is None:
        raise RuntimeError("Failed to download the YouTube video.")
    debug_container.markdown(f"Downloaded file to: `{file_path}`")
    progress_bar.progress(20)

    time, audio_data, sample_rate = extract_drums(file_path)
    progress_bar.progress(60)

    debug_container.markdown("Estimating bass/snare frequencies...")
    bass_drum_freq, snare_freq = identify_bass_and_snare_frequencies(audio_data, sample_rate)
    debug_container.markdown(f"Bass drum: `{bass_drum_freq:.2f}` Hz -- Snare drum: `{snare_freq:.2f}` Hz")
    debug_container.markdown("Identifying blastbeats...")
    progress_bar.progress(80)

    labeled_sections = get_sections_labeled_by_percussion_content_from_audio(time, audio_data, sample_rate,
                                                                             bass_drum_freq, snare_freq)
    blastbeat_intervals = identify_blastbeat_intervals(labeled_sections)
    progress_bar.progress(90)
    debug_container.markdown("Creating figure...")

    return plot_waveform(time, audio_data, blastbeat_intervals, title=file_path.stem)

def main():
    st.set_page_config(page_title="Demo", layout="wide", initial_sidebar_state="expanded")
    st.sidebar.title("Blastbeat Detector")
    st.sidebar.write("Demo UI")
    if st.sidebar.button("Reset"):
        st.session_state.clear()

    url = st.text_input(" ", st.session_state.get("url", "https://www.youtube.com/watch?v=cPTJzeEqkFs"), placeholder="Youtube URL", key="youtube_url")
    st.session_state['url'] = url

    event = st_player(url, **options, key="youtube_player")
    st.sidebar.write(event)

    if url and st.button("Process Song"):
        try:
            progress_bar = st.progress(0)
            debug_container = st.expander("Debug Info", expanded=True)
            fig = process_song(url, progress_bar, debug_container)
            progress_bar.progress(100)
            st.session_state['fig'] = fig
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if 'fig' in st.session_state:
        st.pyplot(st.session_state['fig'], width='stretch')

if __name__ == "__main__":
    main()


