import os
import re
from pathlib import Path

from yt_dlp import YoutubeDL


def download_from_youtube_as_mp3(url: str) -> tuple[bool, Path | None]:
    if not re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/', url):
        raise ValueError("The provided URL is not a valid YouTube video URL.")

    output_folder = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(output_folder, exist_ok=True)

    opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "quiet": True,
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.join(output_folder, f"{info['title']}.mp3")
            return True, Path(file_path) if os.path.exists(file_path) else None
    except Exception as e:
        print(f"Error: {e}")
        return False, None

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=K3rDRsEMay0" # DF - Grotesque Impalement
    success, path = download_from_youtube_as_mp3(test_url)
    if success:
        print(f"Downloaded file path: {path}")
    else:
        print("Failed to download the video.")