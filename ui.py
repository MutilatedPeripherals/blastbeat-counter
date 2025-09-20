import streamlit as st
from streamlit_player import st_player

options = {
    "events": ["onProgress"],
    "progress_interval": 100 # ms
}

def main():
    st.set_page_config(page_title="Blastbeat Detector", layout="wide", initial_sidebar_state="expanded")
    url = st.text_input("", "https://www.youtube.com/watch?v=cPTJzeEqkFs")

    event = st_player(url, **options, key="youtube_player")

    st.sidebar.title("Blastbeat Detector")
    st.sidebar.write("Demo UI")
    st.sidebar.write(event)


if __name__ == "__main__":
    main()